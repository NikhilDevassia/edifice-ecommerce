# Generated by Django 4.0.5 on 2022-07-11 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_mrp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mrp',
            field=models.IntegerField(),
        ),
    ]
