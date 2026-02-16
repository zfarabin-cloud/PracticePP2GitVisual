# function_arguments

# Positional and Keyword Arguments
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")

# Default Parameters
def my_country_function(country = "Norway"):
  print("I am from", country)

my_country_function("Sweden")
my_country_function()

# Positional-Only Arguments
def positional_function(name, /):
  print("Hello", name)

# Keyword-Only Arguments
def keyword_function(*, name):
  print("Hello", name)