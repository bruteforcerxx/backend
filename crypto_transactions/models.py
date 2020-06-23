from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
STATUS = [
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed')
]

TRANSACTION_TYPE = [
    ('debit', 'debit'),
    ('Transfer', 'Transfer')
]


PLATFORM = [
    ('luno', 'luno'),
    ('coinbase', 'coinbase'),
    ('axemo', 'axemo'),
    ('blockchain', 'blockchain')
]

CURRENCY =[
    ('BTC', 'BTC'),
    ('ETH', 'ETH'),
    ('LTC', 'LTC'),
    ('BCH', 'BCH'),
    ('NGN', 'NGN')
]


class DebitTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    tx_hash = models.CharField(max_length=400, blank=True, null=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, choices=TRANSACTION_TYPE, default='debit')
    route = models.CharField(max_length=250, choices=PLATFORM, default='blockchain')
    currency = models.CharField(max_length=250, choices=CURRENCY, default='BTC')
    description = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, default='not provided')
    status = models.CharField(max_length=200, choices=STATUS, default='pending')
    resolve = models.BooleanField(default=False)
    objects = None

    def __str__(self):
        return str(self.user)


class TransferForm(ModelForm):
    class Meta:
        model = DebitTransaction
        fields = ['destination', 'amount', 'description']
