from django.test import TestCase
import time
# Create your tests here.
from coinbase.wallet.client import Client

currency = 'LTC'

key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
client = Client(key, secret)
pair = f'{currency}-NGN'
price = client.get_spot_price(currency_pair=pair)
amount = float(price['amount'])
amount = 1500.00 / amount
amount = float("{:.8f}".format(amount))
print(amount)

# 0.01648939