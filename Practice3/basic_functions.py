# basic_functions

def my_function():
  print("Hello from a function")

def my_function():
  print("Hello from a function")
my_function()

def my_function():
  print("Hello from a function")
my_function()
my_function()
my_function()

'''
Valid function names:
calculate_sum()
_private_function()
myFunction2()
'''

temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)


def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9
print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

def get_greeting():
  return "Hello from a function"
message = get_greeting()
print(message)

def get_greeting():
  return "Hello from a function"
print(get_greeting())

def my_function():
  pass

# Python Function Arguments

def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

def my_function(name): # name is a parameter
  print("Hello", name)
my_function("Emil") # "Emil" is an argument

def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes")

'''
def my_function(fname, lname):
  print(fname + " " + lname) # This function expects 2 arguments, but gets only 1
my_function("Emil")
'''

def my_function(name = "friend"): # default parametre
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

def my_function(country = "Norway"): # default parametre
  print("I am from", country)
my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")

def my_function(animal, name): # key = value syntax, order of arguments doesn't matter
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy")

def my_function(animal, name): # positional argument, order matters
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy")

'''
You can mix positional and keyword arguments in a function call.
However, positional arguments must come before keyword arguments:
'''
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)
my_function("dog", name = "Buddy", age = 5)

def my_function(fruits): # list as argument
  for fruit in fruits:
    print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

def my_function(person): # dict as argument
  print("Name:", person["name"])
  print("Age:", person["age"])
my_person = {"name": "Emil", "age": 25}
my_function(my_person)

# return
def my_function(x, y): 
  return x + y
result = my_function(5, 3)
print(result)

def my_function():
  return ["apple", "banana", "cherry"]
fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

def my_function():
  return (10, 20)
x, y = my_function()
print("x:", x)
print("y:", y)


# Positional-Only Arguments
def my_function(name, /):
  print("Hello", name)
my_function("Emil")

def my_function(name):
  print("Hello", name)
my_function(name = "Emil")

'''
error
def my_function(name, /):
  print("Hello", name)
my_function(name = "Emil")
'''

# Keyword-Only Arguments
def my_function(*, name):
  print("Hello", name)
my_function(name = "Emil")

def my_function(name):
  print("Hello", name)
my_function("Emil")

'''
error
def my_function(*, name):
  print("Hello", name)
my_function("Emil")
'''

# Combining Positional-Only and Keyword-Only

def my_function(a, b, /, *, c, d):
  return a + b + c + d
result = my_function(5, 10, c = 15, d = 20)
print(result)

