# Generated by Django 3.0.6 on 2020-06-23 21:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_transactions', '0013_auto_20200623_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
