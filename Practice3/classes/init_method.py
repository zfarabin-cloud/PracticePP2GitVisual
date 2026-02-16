# init_method

# The __init__ method assigns values to object properties
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

# Using default values in __init__
class PersonDefault:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

# The 'self' parameter can be named anything (like 'myobject')
class PersonCustomSelf:
  def __init__(myobject, name):
    myobject.name = name

# Multi-parameter __init__ (city and country)
class LocationPerson:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country
p_loc = LocationPerson("Linus", 30, "Oslo", "Norway")

# Method calling another method within the same class
class WelcomePerson:
  def __init__(self, name):
    self.name = name
  def greet(self):
    return "Hello, " + self.name
  def welcome(self):
    message = self.greet()
    print(message + "! Welcome to our website.")

# Name Mangling: Accessing private variables (Not Recommended)
class Secret:
  def __init__(self, age):
    self.__age = age
s1 = Secret(30)
print(s1._Secret__age) # Direct access via name mangling

# Computer Composition (Multiple Inner Classes)
class Computer:
  def __init__(self):
    self.cpu = self.CPU()
    self.ram = self.RAM()
  class CPU:
    def process(self): print("Processing data...")
  class RAM:
    def store(self): print("Storing data...")

# Playlist Management (Multiple methods)
class Playlist:
  def __init__(self, name):
    self.name = name
    self.songs = []
  def add_song(self, song): self.songs.append(song)
  def remove_song(self, song): self.songs.remove(song)