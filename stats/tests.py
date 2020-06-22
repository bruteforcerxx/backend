from django.test import TestCase

# Create your tests here.
import string
import random

def get_referral_code(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

print(get_referral_code(stringLength=8))