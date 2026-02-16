# class_methods

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  # Instance method
  def greet(self):
    print("Hello, my name is " + self.name)

  # The __str__ method controls what is returned when the object is printed
  def __str__(self):
    return f"{self.name} ({self.age})"

p1 = Person("Tobias", 36)
p1.greet()
print(p1)