# Generated by Django 4.0.5 on 2022-07-15 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_used', models.BooleanField(default=False)),
                ('date_used', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(null=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
