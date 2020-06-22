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
    ('debit', 'debit')
]


PLATFORM = [
    ('luno', 'luno'),
    ('coinbase', 'coinbase'),
    ('axemo', 'axemo'),
    ('blockchain', 'blockchain')
]


class DebitTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    tx_hash = models.CharField(max_length=400, blank=True, null=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, choices=TRANSACTION_TYPE, default='debit')
    platform = models.CharField(max_length=250, choices=PLATFORM, default='blockchain')
    description = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')
    resolve = models.BooleanField(default=False)
    objects = None

    def __str__(self):
        return str(self.user)


class TransferForm(ModelForm):
    class Meta:
        model = DebitTransaction
        fields = ['destination', 'amount', 'description']
