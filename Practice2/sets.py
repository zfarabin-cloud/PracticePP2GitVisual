# sets

thisset = {"apple", "banana", "cherry"}
print(thisset)

thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)

thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)

thisset = {"apple", "banana", "cherry", False, True, 0}
print(thisset)

thisset = {"apple", "banana", "cherry"}
print(len(thisset))

set1 = {"apple", "banana", "cherry"}
set2 = {1, 5, 7, 9, 3}
set3 = {True, False, False}

set1 = {"abc", 34, True, 40, "male"}

myset = {"apple", "banana", "cherry"}
print(type(myset))

thisset = set(("apple", "banana", "cherry")) # note the double round-brackets
print(thisset)

# Access Set Items
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)

thisset = {"apple", "banana", "cherry"}
print("banana" in thisset)

# Add Set Items
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)

thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)

# Remove Set Items
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana") #If the item to remove does not exist, remove() will raise an error.
print(thisset)

thisset = {"apple", "banana", "cherry"}
thisset.discard("banana") #If the item to remove does not exist, discard() will NOT raise an error.
print(thisset)

thisset = {"apple", "banana", "cherry"}
x = thisset.pop() #Remove random item
print(x)
print(thisset)

thisset = {"apple", "banana", "cherry"}
thisset.clear()
print(thisset)
# del thisset

# Loop Sets
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)

# Join Sets
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)
print(set3)

set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set1.update(set2)
print(set1)

x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
x.intersection_update(y)
print(x)

x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
x.symmetric_difference_update(y)
print(x)

x = {"apple", "banana", "cherry", True}
y = {"google", 1, "apple", 2}
z = x.symmetric_difference(y)
print(z)

# frozenset
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

# set methods
s1, s2 = {1, 2}, {2, 3}
s1.add(4)                          # Add element
s1.discard(4)                      # Remove specified item
s1.remove(1)                       # Remove specified element
s1.pop()                           # Remove an element
print(s1.union(s2))                # Return union of sets
s1.update(s2)                      # Update set with union
print(s1.intersection(s2))         # Return intersection
s1.intersection_update(s2)         # Remove items not in both
print(s1.difference(s2))           # Return difference
s1.difference_update(s2)           # Remove shared items
print(s1.symmetric_difference(s2)) # Return symmetric difference
s1.symmetric_difference_update(s2) # Insert symmetric differences
print(s1.isdisjoint(s2))           # Check if intersection is empty
print(s1.issubset(s2))             # Check if s1 is in s2
print(s1.issuperset(s2))           # Check if s2 is in s1
s1_copy = s1.copy()                # Return copy of set
s1.clear()                         # Remove all elements