# map_filter_reduce.py
from functools import reduce

# Sample data
numbers = [1, 2, 3, 4, 5, 6]

# 1. map: Apply a function to every item (e.g., squaring numbers)
squared = list(map(lambda x: x**2, numbers))
print(f"Squared: {squared}")

# 2. filter: Keep items that meet a condition (e.g., even numbers)
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# 3. reduce: Combine all items into a single value (e.g., sum)
total_sum = reduce(lambda x, y: x + y, numbers)
print(f"Total Sum: {total_sum}")