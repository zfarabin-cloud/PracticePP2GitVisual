#Write a Python program that matches a string that has an 'a' followed by two to three 'b'

import re
text = "msdfnsjandaasacaabbbsdfsdsd"
x = re.search('abb|abbb', text)
print(x)