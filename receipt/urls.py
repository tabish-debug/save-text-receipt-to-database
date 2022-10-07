from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import CRUD

app_name = 'receipt-api'

urlpatterns = [
    path('crud', CRUD.as_view(), name="crud")
]
