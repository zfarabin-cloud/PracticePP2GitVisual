# generators

# Python Iterators
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)
print(next(myit))
print(next(myit))
print(next(myit))


mystr = "banana"
myit = iter(mystr)
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))


mytuple = ("apple", "banana", "cherry")
for x in mytuple:
  print(x)


mystr = "banana"
for x in mystr:
  print(x)


class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))


class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)
for x in myiter:
  print(x)


# Create a generator that generates the squares of numbers up to some number N.
def generate_squares(N):
    for i in range(N + 1):
        yield i ** 2

for num in generate_squares(5):
     print(num)

# Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i  # Yielding just int

n = int(input("Enter n: "))
print(*even_generator(n), sep=",")

# Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print(list(divisible_by_3_and_4(24)))

# Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for value in squares(2, 6):
    print(value)

# Implement a generator that returns all numbers from (n) down to 0.
def countdown(n):
    for i in range(n, -1, -1):
        yield i

for num in countdown(5):
    print(num)

