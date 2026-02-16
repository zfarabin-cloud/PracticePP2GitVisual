# lambda_basics

# Simple lambda functions
add_ten = lambda a : a + 10
multiply = lambda a, b : a * b

# Lambda as a function factory
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
print(mydoubler(11))

# Lambda with three arguments
sum_three = lambda a, b, c : a + b + c
print(sum_three(5, 6, 2))
