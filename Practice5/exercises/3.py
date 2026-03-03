#Write a Python program to find sequences of lowercase letters joined with a underscore.

import re
text = 'shdhiwi_jd_ij_di_dksdkals_smam'
x = re.findall('[a-z]*_', text)
print(x)