# class_definition

# Basic class definition
class MyClass:
  x = 5

p1 = MyClass()
print(p1.x)

# Empty class using pass
class Person:
  pass

# Inner Class Example
class Outer:
  def __init__(self):
    self.name = "Outer"

  class Inner:
    def __init__(self):
      self.name = "Inner"

    def display(self):
      print("Hello from inner class")

outer_obj = Outer()
inner_obj = outer_obj.Inner()


# Deleting an object and multiple instantiation
class MyClass:
  x = 5
p1 = MyClass()
del p1 
p2 = MyClass()
p3 = MyClass()