from django.db import models
from django.db.models import DateTimeField


# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.TextField()
    role = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.user_id)

class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=13)
    customer_email = models.EmailField()
    customer_type = models.CharField(max_length=255, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.customer_id)


class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category_id)


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE
    )
    product_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    price = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)
