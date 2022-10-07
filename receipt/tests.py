from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from .analyizer.block_position import GetPositionOfBlocks
from authentication.serializers import RegisterSerializer

User = get_user_model()

test_blocks = [
    {
        'begin_row': 1,
        'begin_col': 16,
        'end_row': 4,
        'end_col': 24
    },
    {
        'begin_row': 8,
        'begin_col': 1,
        'end_row': 8,
        'end_col': 42
    },
    {
        'begin_row': 11,
        'begin_col': 1,
        'end_row': 14,
        'end_col': 42
    },
    {
        'begin_row': 18,
        'begin_col': 1,
        'end_row': 18,
        'end_col': 22
    },
    {
        'begin_row': 20,
        'begin_col': 1,
        'end_row': 20,
        'end_col': 43
    },
    {
        'begin_row': 24,
        'begin_col': 1,
        'end_row': 25,
        'end_col': 44
    },
    {
        'begin_row': 29,
        'begin_col': 14,
        'end_row': 39,
        'end_col': 33
    },
    {
        'begin_row': 44,
        'begin_col': 10,
        'end_row': 44,
        'end_col': 27
    }
]

class PositionTestCase(APITestCase):
    def setUp(self) -> None:
        with open('test_receipt_sample.txt', 'r') as file:
            data = file.read()
            blocks = GetPositionOfBlocks(data=data)
            self.blocks = blocks()

        self.test_blocks = test_blocks

    def test_block1_position(self):
        self.assertEqual(self.blocks[0], self.test_blocks[0])

    def test_block2_position(self):
        self.assertEqual(self.blocks[1], self.test_blocks[1])

    def test_block3_position(self):
        self.assertEqual(self.blocks[2], self.test_blocks[2])

    def test_block4_position(self):
        self.assertEqual(self.blocks[3], self.test_blocks[3])

    def test_block5_position(self):
        self.assertEqual(self.blocks[4], self.test_blocks[4])

    def test_block6_position(self):
        self.assertEqual(self.blocks[5], self.test_blocks[5])

    def test_block7_position(self):
        self.assertEqual(self.blocks[6], self.test_blocks[6])

    def test_block8_position(self):
        self.assertEqual(self.blocks[7], self.test_blocks[7])

class CRUDTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.register_valid_data = {
            'username': 'refive',
            'email': 'info@refive.com',
            'password': '123456789',
        }

        self.regitser_invalid_data = {
            'email': 'info@refive.com',
            'password': '12346546444'
        }

        user = RegisterSerializer(data=self.register_valid_data)
        user.is_valid(raise_exception=True)
        user.save()

        self.user = User.objects.get(email=user.data['email'])
        self.user.is_verify = True
        self.user.save()

        self.client.force_authenticate(user=self.user)
        self.test_blocks = test_blocks        

    def test_upload_text_file(self):
        with open('test_receipt_sample.txt', 'r') as file:
            response = self.client.post(reverse('receipt-api:crud'), data={ 'file': file })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'blocks': self.test_blocks})

    def test_get_receipt(self):
        with open('test_receipt_sample.txt', 'r') as file:
            self.client.post(reverse('receipt-api:crud'), data={ 'file': file })
        
        response = self.client.get(reverse('receipt-api:crud'))
        self.assertEqual(response.status_code, 200)

        data = response.data
        receipt = data['results'][0]
        receipt_products = receipt['products']

        self.assertEqual(data['count'], 1)
        
        self.assertIn('products', receipt)
        self.assertIn('payment', receipt)
        self.assertIn('information', receipt)
        self.assertIn('bill_no', receipt)

        self.assertEqual(len(receipt_products), 4)


    def test_delete_receipt(self):
        with open('test_receipt_sample.txt', 'r') as file:
            response = self.client.post(reverse('receipt-api:crud'), data={ 'file': file })  
        
        response = self.client.get(reverse('receipt-api:crud'))
        data = response.data
        receipt = data['results'][0]
        receipt_id = receipt['id']

        response = self.client.delete(reverse('receipt-api:crud'), **{'QUERY_STRING': f'receipt_id={receipt_id}'})

        self.assertEqual(response.status_code, 204)
    