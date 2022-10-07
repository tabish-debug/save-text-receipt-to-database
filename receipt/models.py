from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Receipt(models.Model):
    company_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)
    bill_no = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')

    def __str__(self) -> str:
        return self.company_name

class Product(models.Model):
    quantity = models.IntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField(null=False)
    total = models.FloatField(null=False)
    type = models.CharField(max_length=5, null=False)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self) -> str:
        return self.name

class Payment(models.Model):
    grand_total = models.FloatField(null=False)
    payment_method = models.CharField(max_length=30, null=False)
    paid_price = models.FloatField(null=False)
    tax_percentage = models.IntegerField(null=False)
    gross = models.FloatField(null=False)
    net = models.FloatField(null=False)
    tax_price = models.FloatField(null=False)
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, related_name='payment', null=True)

    def __str__(self) -> str:
        return self.payment_method

class Information(models.Model):
    table = models.CharField(max_length=30, null=False)
    terminal = models.CharField(max_length=30, null=False)
    tse_transaktion = models.IntegerField(null=False)
    tse_signatur_nr = models.IntegerField(null=False)
    tse_start = models.DateTimeField(null=False)
    tse_stop = models.DateTimeField(null=False)
    tse_seriennummer = models.CharField(max_length=80, null=False)
    tse_zeitformat = models.CharField(max_length=20)
    tse_signatur = models.CharField(max_length=50, null=False)
    tse_hashalgorithmus = models.CharField(max_length=20, null=False)
    tse_status = models.CharField(max_length=20, null=False)
    ust_id = models.CharField(max_length=30, null=False)
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, related_name='information', null=True)

    def __str__(self) -> str:
        return self.table
