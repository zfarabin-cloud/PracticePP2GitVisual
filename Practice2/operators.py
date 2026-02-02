# operators

# Arithmetic Operators
print(10 + 5)

sum1 = 100 + 50      # 150 (100 + 50)
sum2 = sum1 + 250    # 400 (150 + 250)
sum3 = sum2 + sum2   # 800 (400 + 400)

x = 15
y = 4
print(x + y) # add
print(x - y) # minus
print(x * y) # multiply
print(x / y) # Division always returns a float
print(x % y) # остаток
print(x ** y) # Exponentiation
print(x // y) # Floor division always returns an integer. It rounds DOWN to the nearest integer

# Assignment Operators
x = 10          # =   (Assignment)
x += 3          # +=  (Add): x = 10 + 3 = 13
x -= 2          # -=  (Subtract): x = 13 - 2 = 11
x *= 4          # *=  (Multiply): x = 11 * 4 = 44
x /= 2          # /=  (Divide): x = 44 / 2 = 22.0
x %= 7          # %=  (Modulus/Remainder): 22 % 7 = 1.0
x //= 0.5       # //= (Floor Division): 1.0 // 0.5 = 2.0
x **= 3         # **= (Exponent): 2.0^3 = 8.0

# Bitwise Assignment
x = int(x)      # Convert to int (8) for bitwise examples
x &= 12         # &=  (Bitwise AND): 8 & 12 = 8
x |= 2          # |=  (Bitwise OR): 8 | 2 = 10
x ^= 1          # ^=  (Bitwise XOR): 10 ^ 1 = 11
x >>= 1         # >>= (Right Shift): 11 >> 1 = 5
x <<= 2         # <<= (Left Shift): 5 << 2 = 20

# Walrus Operator
numbers = [1, 2, 3, 4, 5]
if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

# Comparison Operators
x = 5
y = 3
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

x = 5
print(1 < x < 10)
print(1 < x and x < 10)

# Logical Operators
x = 5
print(x > 0 and x < 10)
print(x < 5 or x > 10)
print(not(x > 3 and x < 10))

# Identity Operators
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)
print(x == y)

x = ["apple", "banana"]
y = ["apple", "banana"]
print(x is not y)

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y) #equal
print(x is y) #same

# Membership Operators
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)

fruits = ["apple", "banana", "cherry"]
print("pineapple" not in fruits)

text = "Hello World"
print("H" in text)
print("hello" in text)
print("z" not in text)

# Bitwise Operators
x, y = 10, 4
print(x & y) # AND: 1 if both bits are 1
print(x | y) # OR: 1 if at least one bit is 1
print(x ^ y) # XOR: 1 if only one bit is 1
print(~x) # NOT: Inverts all bits
print(x << 2) # Left Shift: Push zeros from right
print(x >> 2) # Right Shift: Push copies of leftmost bit from left

# Operator Precedence
print((6 + 3) - (6 + 3))
print(100 + 5 * 3)