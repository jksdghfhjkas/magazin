# Generated by Django 5.1.2 on 2024-11-24 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0006_remove_globalcategory_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='parser.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='reviewratingproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='parser.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='stockwarehouses',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='parser.product', verbose_name='продукт'),
        ),
    ]
