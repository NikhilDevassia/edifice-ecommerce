# Generated by Django 4.0.5 on 2022-07-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_category',
            name='count_sold',
            field=models.IntegerField(default=0),
        ),
    ]
