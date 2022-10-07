from django.contrib import admin

from .models import Receipt, Product, Payment, Information

admin.site.register(Receipt)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Information)
