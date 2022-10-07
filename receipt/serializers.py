from rest_framework import serializers

from .models import Receipt, Product, Payment, Information

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    payment = PaymentSerializer(many=False)
    information = InformationSerializer(many=False)
    
    class Meta:
        model = Receipt
        fields = [
            'id', 'company_name', 'address', 'bill_no', 'created_at', 
            'products', 'payment', "information", "created_by"
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        payment_data = validated_data.pop('payment')
        information_data = validated_data.pop('information')

        receipt = Receipt.objects.create(**validated_data)

        payment_data.update({ 'receipt': receipt })
        information_data.update({ 'receipt': receipt }) 

        Payment.objects.create(**payment_data)
        Information.objects.create(**information_data)

        for product in products_data:
            product = Product.objects.create(**product)
            receipt.products.add(product)
        return receipt
