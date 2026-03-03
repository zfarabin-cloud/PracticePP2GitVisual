#Write a Python program to convert a given camel case string to snake case.

import re
def com(s):
    res = ''
    if s.group(1):
        res += (s.group(1)).lower()
    else:
        res += ('_' + s.group(2)).lower()
    return res
s = input()
snake = re.sub(r'(^[A-Z]| [A-Z])|([A-Z])', com, s) 
print(snake)