# method_overriding

class Vehicle:
  def move(self):
    print("Move!")

class Car(Vehicle):
  def move(self):
    print("Drive!")

class Boat(Vehicle):
  def move(self):
    print("Sail!")

# Different objects using the same method name (Polymorphism)
for x in (Car(), Boat()):
  x.move()