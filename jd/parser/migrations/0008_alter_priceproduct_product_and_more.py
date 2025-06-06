# Generated by Django 5.1.2 on 2024-11-26 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0007_alter_priceproduct_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='price_db', to='parser.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='reviewratingproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating_db', to='parser.product', verbose_name='продукт'),
        ),
    ]
