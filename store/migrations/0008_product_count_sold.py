# Generated by Django 4.0.5 on 2022-07-24 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_count_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_sold',
            field=models.IntegerField(default=0),
        ),
    ]
