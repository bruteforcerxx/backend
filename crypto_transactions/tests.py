from django.test import TestCase

# Create your tests here.
user = "['a', 'b']"
print(type(user))
print(type(eval(user)))
