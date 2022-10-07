from django.conf import settings

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .analyizer import get_position_of_blocks, get_receipt_data
from .serializers import ReceiptSerializer
from .models import Receipt

class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'

class CRUD(generics.DestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = ResultsSetPagination

    def post(self, request):
        data = request.FILES['file']

        if not self.is_valid_extension(data):
            return Response(
                data=dict(message='extension not allowed'), 
                status=status.HTTP_404_NOT_FOUND
            )

        file_data = data.file.read().decode('utf-8')
        positions = get_position_of_blocks(file_data)
        receipt = get_receipt_data(file_data)

        receipt_serializer = self.serializer_class(data={
            'company_name': receipt['company_name'],
            'address': receipt['address'],
            'bill_no' : receipt['bill_no'],
            'created_at': receipt['created_at'],
            'created_by': request.user.id,
            'products': receipt['products'],
            'payment': receipt['payment'],
            'information': receipt['information']           
        })

        receipt_serializer.is_valid(raise_exception=True)
        receipt_serializer.save()

        return Response(
            data=dict(blocks=positions),
            status=status.HTTP_201_CREATED)

    def is_valid_extension(self, data):
        filename = data.name
        _, ext = filename.split('.') 
        if ext in settings.IMAGE_FILE_FORMATS:
            return True
        return False

    def get(self, request):
        user = request.GET.get("user", None)

        if user:
            receipts = request.user.receipts
            serializer = self.serializer_class(receipts, many=True, )
            data = serializer.data
            return self.get_paginated_response(self.paginate_queryset(data))

        serializer = self.serializer_class(self.queryset.all(), many=True)
        data = serializer.data

        return self.get_paginated_response(self.paginate_queryset(data))

    def delete(self, request):
        receipt_id = int(request.GET['receipt_id'])
        user = request.user
        
        receipt = Receipt.objects.filter(id=receipt_id, created_by=user).first()
        
        if not receipt:
            data = dict(message="receipt not found")
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        receipt.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
            