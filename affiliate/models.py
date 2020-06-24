from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random


# Create your models here.
LEVEL = [
    ('standard', 'standard'),
    ('pro', 'pro'),
    ('premium', 'premium')
]


def ref_code():
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for _ in range(10))
    link = f'http://127.0.0.1:8000/home/register/{code}'
    return [code, link]


class Agent(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    referral_code = models.CharField(max_length=250, default=ref_code()[0])
    referral_link = models.CharField(max_length=250, default=ref_code()[1])
    fee_paid = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    agent_level = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    rank = models.CharField(max_length=250, choices=LEVEL, default='standard')
    primary_down_lines = models.TextField(default=[])
    secondary_down_lines = models.TextField(default=[])
    total_primary_down_lines = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    total_secondary_down_lines = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    objects = None

    def __str__(self):
        return str(self.name)
