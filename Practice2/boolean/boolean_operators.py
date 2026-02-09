# boolean_operators

# isinstance check
x = 200
print(isinstance(x, int))

# Logical Operators: and, or, not
a = 200
b = 33
c = 500

if a > b and c > a:
  print("Both conditions are True")

if a > b or a > c:
  print("At least one of the conditions is True")

if not a > b:
  print("a is NOT greater than b")