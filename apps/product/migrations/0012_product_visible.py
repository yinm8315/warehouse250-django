# Generated by Django 3.2.4 on 2021-06-19 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
