from django.test import TestCase
import time
import datetime
import json
import requests

x = '2020-07'
print(x[5:])
print(x[:4])

response = requests.get('https://ravesandboxapi.flutterwave.com/mockvbvpage?ref=FLW-MOCK-'
                   'e285215fd322046a996d7d53e6bcedc2&code=00&message=Approved.%20Successful&receiptno=RN1593937528754')
print(response)
