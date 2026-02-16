# class_variables

class Student:
  species = "Human"  # Class Variable shared by all instances

  def __init__(self, name):
    self.name = name      # Instance Variable
    self.__grade = 0      # Private Variable (Encapsulation)
    self._salary = 50000  # Protected Variable

  # Getter and Setter for private variable
  def set_grade(self, grade):
    if 0 <= grade <= 100:
      self.__grade = grade

  def get_grade(self):
    return self.__grade