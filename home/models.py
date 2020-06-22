from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

# Create your models here.


class UsersData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    bitcoin_balance = models.FloatField(default=0.00000000)
    etherum_balance = models.FloatField(default=0.00000000)
    litecoin_balance = models.FloatField(default=0.00000000)
    bitcoin_cash_balance = models.FloatField(default=0.00000000)
    local_currency_balance = models.DecimalField(max_digits=50, decimal_places=3, default=0.000)
    vault_balance = models.DecimalField(max_digits=50, decimal_places=8, default=0.0000000)
    vault_release_date = models.DateTimeField(default=timezone.now)
    referral = models.EmailField(max_length=250, blank=True, null=True)
    agent_status = models.CharField(max_length=400, default='level 0')
    objects = None

    def __str__(self):
        return str(self.user)


class RegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'username']

