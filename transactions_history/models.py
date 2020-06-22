from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    btc_history = models.TextField(default='{}')
    eth_history = models.TextField(default='{}')
    ltc_history = models.TextField(default='{}')
    bch_history = models.TextField(default='{}')
    ngn_history = models.TextField(default='{}')
    objects = None

    def __str__(self):
        return str(self.user)
