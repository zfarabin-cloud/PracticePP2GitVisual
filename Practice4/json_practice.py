# json

# JSON in Python
import json

'''
JSON is a syntax for storing and exchanging data.

JSON is text, written with JavaScript object notation.
'''

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
# parse x:
y = json.loads(x)
# the result is a Python dictionary: (data mapping)
print(y["age"])


# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
# convert into JSON:
y = json.dumps(x)
# the result is a JSON string:
print(y)


print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))


x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
print(json.dumps(x))


# Format the result
x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

# use four indents to make it easier to read the result:
print(json.dumps(x, indent=4))

# use . and a space to separate objects, and a space, a = and a space to separate keys from their values:
print(json.dumps(x, indent=4, separators=(". ", " = ")))

# sort the result alphabetically by keys:
print(json.dumps(x, indent=4, sort_keys=True))


# Exercise

# 1. Open and read the JSON file
with open(r'c:\Users\Farabi\Desktop\PracticePP2VS\PracticePP2GitVisual\Practice4\sample-data.json', 'r') as file:
    data = json.load(file)

# 2. Print the headers matching the requested format
print("Interface Status")
print("=" * 80)
print("{:<50} {:<20} {:<8} {:<6}".format("DN", "Description", "Speed", "MTU"))
print("{:<50} {:<20} {:<8} {:<6}".format("-" * 50, "-" * 20, "-" * 6, "-" * 6))

# 3. Extract and print the data rows
for item in data['imdata']:
    attributes = item['l1PhysIf']['attributes']
    
    dn = attributes.get('dn', '')
    descr = attributes.get('descr', '')
    speed = attributes.get('speed', '')
    mtu = attributes.get('mtu', '')
    
    print("{:<50} {:<20} {:<8} {:<6}".format(dn, descr, speed, mtu))