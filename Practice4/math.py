# math

# Python Math

x = min(5, 10, 25)
y = max(5, 10, 25)
print(x)
print(y)

x = abs(-7.25)
print(x)

x = pow(4, 3)
print(x)

# The Math Module
import math
x = math.sqrt(64)
print(x) # 8

x = math.ceil(1.4)
y = math.floor(1.4)
print(x) # returns 2
print(y) # returns 1

x = math.pi
print(x)


# Write a Python program to convert degree to radian.
degree = 15
radian = math.radians(degree)
print(f"Input degree: {degree}")
print(f"Output radian: {radian:.6f}")

# Write a Python program to calculate the area of a trapezoid.
height = 5
base1 = 5
base2 = 6
area = 0.5 * height * (base1 + base2)
print(f"Height: {height}")
print(f"Base, first value: {base1}")
print(f"Base, second value: {base2}")
print(f"Expected Output: {area}")

# Write a Python program to calculate the area of regular polygon.
n = 4
s = 25
area = (n * (s ** 2)) / (4 * math.tan(math.pi / n))
print(f"Input number of sides: {n}")
print(f"Input the length of a side: {s}")
print(f"The area of the polygon is: {area:g}")

# Write a Python program to calculate the area of a parallelogram.
base = 5
height = 6
area = float(base * height)

print(f"Length of base: {base}")
print(f"Height of parallelogram: {height}")
print(f"Expected Output: {area}")
