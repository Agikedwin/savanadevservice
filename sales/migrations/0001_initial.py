# Generated by Django 5.2.1 on 2025-05-29 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_contact', models.CharField(max_length=13)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_type', models.CharField(default=1, max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_type', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('password', models.TextField()),
                ('role', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.productcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.users')),
            ],
        ),
        migrations.AddField(
            model_name='productcategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.users'),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customers')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.users')),
            ],
        ),
        migrations.AddField(
            model_name='customers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.users'),
        ),
    ]
