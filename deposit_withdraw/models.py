from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

# Create your models here.
STATUS = [
    ('pending', 'pending'),
    ('complete', 'successful'),
    ('failed', 'failed')
]


METHOD = [
    ('debit card', 'debit card'),
    ('transfer', 'transfer')
]


CURRENCY = [
    ('bitcoin', 'bitcoin'),
    ('etherum', 'etherum'),
    ('litecoin', 'litecoin'),
    ('bitcoincash', 'bitcoincash')
]


class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, default='Buy')
    description = models.CharField(max_length=250, blank=True, null=True)
    currency = models.CharField(max_length=250, choices=CURRENCY, default='Bitcoin')
    status = models.CharField(max_length=200, choices=STATUS, default='pending')
    method = models.CharField(max_length=200, choices=METHOD, default='debit card')

    def __str__(self):
        return self.user


class Sell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, default='Sell')
    description = models.CharField(max_length=250, blank=True, null=True)
    currency = models.CharField(max_length=250, choices=CURRENCY, default='Bitcoin')
    status = models.CharField(max_length=200, choices=STATUS, default='pending')

    def __str__(self):
        return self.user


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, default='Deposit')
    description = models.CharField(max_length=250, blank=True, null=True)
    bank = models.CharField(max_length=250, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')

    def __str__(self):
        return self.user


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, default='withdraw')
    description = models.CharField(max_length=250, blank=True, null=True)
    account_number = models.CharField(max_length=250, null=True)
    bank = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')

    def __str__(self):
        return self.user


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, default='bank')
    description = models.CharField(max_length=250, blank=True, null=True)
    destination_account = models.CharField(max_length=250, null=True)
    bank = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')

    def __str__(self):
        return self.user

