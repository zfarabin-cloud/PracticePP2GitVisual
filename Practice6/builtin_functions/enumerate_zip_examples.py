# enumerate_zip_examples.py
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

# 1. enumerate: Get index and value at the same time
print("Student Roster:")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

# 2. zip: Combine two or more lists element-wise
print("\nStudent Grades:")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Creating a dictionary from two lists using zip
score_dict = dict(zip(names, scores))
print(f"\nDictionary format: {score_dict}")