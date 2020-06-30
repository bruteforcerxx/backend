from django.test import TestCase

# Create your tests here.

x = '3621236.00'
url('https://image.ibb.co/bVnMrc/g3095.png'),
print(len(x))
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
    b = x[0:3]
    c = x[3:]
    d = f'{a},{b},{c}'
    print(c)