# boolean_intro

print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15
print(bool(x))
print(bool(y))

# Values that evaluate to True
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# Values that evaluate to False
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# Objects with __len__ returning 0 evaluate to False
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

def myFunction():
  return True
print(myFunction())