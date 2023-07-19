import random

from django.test import TestCase

# Create your tests here.


ips = []
with open('ip.txt', 'rb') as f:
    lines = f.readlines()
    for line in lines:
        ips.append(str(line).strip().replace('b\'', '').replace('\\n\'', ''))
print(ips)