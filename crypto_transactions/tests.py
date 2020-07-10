from django.test import TestCase
from rave_python import Rave
import requests


# Create your tests here.

x = '382982828.00'

if len(x) == 7:
    a = x[0]
    b = x[1:]
    c = f'{a},{b}'
    print(c)
elif len(x) == 8:
    a = x[:2]
    b = x[2:]
    c = f'{a},{b}'
    print(c)
elif len(x) == 9:
    a = x[:3]
    b = x[3:]
    c = f'{a},{b}'
    print(c)
elif len(x) == 10:
    a = x[0]
    b = x[1:4]
    c = x[4:]
    d = f'{a},{b},{c}'
    print(20)
    print(d)
    print(x)
elif len(x) == 11:
    a = x[:2]
    b = x[2:5]
    c = x[5:]
    d = f'{a},{b},{c}'
    print(20)
    print(d)
    print(x)
elif len(x) == 12:
    a = x[:2]
    b = x[2:5]
    c = x[5:]
    d = f'{a},{b},{c}'
    print(20)
    print(d)
    print(x)
else:
    print(x)

# fee = requests.get('https://bitcoinfees.earn.com/api/v1/fees/recommended').json()
# print(fee)
