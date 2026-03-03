#Write a Python program to replace all occurrences of space, comma, or dot with a colon.

import re
text = 'uduahwudhuahd idnwaundunaund,ad udwna..undunau'
x = re.sub("[.]|[,]|[ ]", ":", text)   #[] return a match for any character of string
print(x)