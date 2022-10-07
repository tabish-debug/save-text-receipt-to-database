import json

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer

User = get_user_model()

class UserTestCase(APITestCase):
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

        self.user = RegisterSerializer(data=self.register_valid_data)
        self.user.is_valid(raise_exception=True)
        self.user.save()

        user = User.objects.get(email=self.user.data['email'])
        user.is_verify = True
        user.save()

        email = self.register_valid_data['email']
        password = self.register_valid_data['password']

        self.login(email, password)

    def login(self, email, password):
        self.client.login(email=email, password=password)

    def test_user_register(self):
        self.user = None

        def _feeder(data):
            self.user = RegisterSerializer(data=data)
            if self.user.is_valid():
                self.user.save()
                user = User.objects.get(email=self.user.data['email'])
                user.is_verify = True
                user.save()
                return self.user
            
            return None
 
        _feeder(self.register_valid_data)
        self.assertEquals(self.user.data['email'], self.register_valid_data['email'])

        invalid_data = _feeder(self.regitser_invalid_data)
        self.assertIsNone(invalid_data)

    def test_user_login(self):
        valid_data = {
            "email": self.user.data['email'],
            "password": "123456789"
        }

        invalid_data = [
            {
                "email": self.user.data['email'],
                "password": "test_!"
            },
            {
                "email": self.user.data['email'],
                "password": ""
            },
            {
                "email": "",
                "password": "aba"
            }
        ]


        def _feeder(data):
            return self.client.post(reverse('user-api:login'), 
                data=json.dumps(data), content_type='application/json')

        login_success = _feeder(data=valid_data)
        self.assertEqual(login_success.status_code, 200)

        for idx in range(0, len(invalid_data)):
            login_fail = _feeder(data=invalid_data[idx])
            err_msg = login_fail.json()
            self.assertEqual(login_fail.status_code, 400)
            if('non_field_errors' in err_msg):
                if idx == 0:
                    self.assertIn('Unable to log in', err_msg['non_field_errors'][0])
                else: 
                    self.assertIn('Email and Password', err_msg['non_field_errors'][0])
