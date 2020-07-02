from django.test import TestCase
import time
import datetime

currentDT = datetime.datetime.now()
x = str(currentDT)[:16]
print(x)
