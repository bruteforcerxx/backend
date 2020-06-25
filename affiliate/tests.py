from django.test import TestCase
import string
import random

# Create your tests here.


def ref_code():
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for _ in range(10))
    link = f'http://127.0.0.1:8000/home/register/{code}'
    return [code, link]


print(ref_code())