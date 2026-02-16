# basic_functions

# Simple function definition and execution
def my_function():
  print("Hello from a function")

my_function()

# Valid naming conventions
'''
Valid function names:
calculate_sum()
_private_function()
myFunction2()
'''

# Example of logic before functionalization
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

# Scope: Local, Global, and Nonlocal
x = "global"

def outer():
  x = "enclosing"
  def inner():
    x = "local"
    print("Inner:", x)
  inner()
  print("Outer:", x)

# Global Keyword
def myfunc():
  global x
  x = 300