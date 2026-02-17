# args_kwargs

# *args for arbitrary positional arguments
def sum_all(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total
result1 = sum_all(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(result1)

# **kwargs for arbitrary keyword arguments
def user_details(**details):
  for key, value in details.items():
    print(key + ":", value)
user_details(name="Alice", age=25, city="Berlin", job="Engineer")

# Unpacking arguments
numbers = [1, 2, 3]
def triple_add(a, b, c): return a + b + c
print(triple_add(*numbers))

# Finding max value using *args
def find_max(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num
print(find_max(3, 7, 2, 9, 1))