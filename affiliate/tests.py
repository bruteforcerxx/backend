from django.test import TestCase
import string
import random

# Create your tests here.

from coinbase.wallet.client import Client

key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"

client = Client(key, secret)
accounts = client.get_accounts()

print(accounts)

eth = "181fc56c-73d6-568e-ab6d-1c0aedc9f333"
ltc = "7c31f848-dc67-5510-8ff4-0e5e74a700c6"
bch = "b38fa818-27f2-5fe2-822f-0d24ab658ee1"