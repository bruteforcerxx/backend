# Generated by Django 3.0.6 on 2020-06-23 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crypto_transactions', '0011_auto_20200623_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('currency', models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('BCH', 'BCH'), ('NGN', 'NGN')], default='BTC', max_length=250)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]