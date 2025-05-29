from django.contrib import admin
from .models import Users, Customers, ProductCategory, Products, Orders
from oauth2login.models import SavanaDiscordUsers

admin.site.register(Users)
admin.site.register(Customers)
admin.site.register(ProductCategory)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(SavanaDiscordUsers)

#Register your models here.


