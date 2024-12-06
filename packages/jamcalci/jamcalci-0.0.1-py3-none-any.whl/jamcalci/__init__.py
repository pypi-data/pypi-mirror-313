
# Arithmetic Operations
def add_numbers(num1, num2):
    return num1 + num2

def subtract_numbers(num1, num2):
    return num1 - num2

def multiply_numbers(num1, num2):
    return num1 * num2

def divide_numbers(num1, num2):
    return num1 / num2

def modulus(num1, num2):
    return num1 % num2

def power(num1, num2):
    return num1 ** num2

def floor_division(num1, num2):
    return num1 // num2

def square(num):
    return num ** 2

def cube(num):
    return num ** 3

def absolute(num):
    return abs(num)

def negate(num):
    return -num

def maximum(num1, num2):
    return max(num1, num2)

def minimum(num1, num2):
    return min(num1, num2)

def average(num1, num2):
    return (num1 + num2) / 2

# Geometric Operations
def area_of_circle(radius):
    return 3.14159 * (radius ** 2)

def circumference_of_circle(radius):
    return 2 * 3.14159 * radius

def area_of_rectangle(length, breadth):
    return length * breadth

def perimeter_of_rectangle(length, breadth):
    return 2 * (length + breadth)

def area_of_triangle(base, height):
    return 0.5 * base * height

def perimeter_of_triangle(a, b, c):
    return a + b + c

def area_of_square(side):
    return side ** 2

def perimeter_of_square(side):
    return 4 * side

def area_of_parallelogram(base, height):
    return base * height

def area_of_trapezium(a, b, height):
    return 0.5 * (a + b) * height

# Statistical Operations
def mean(numbers):
    return sum(numbers) / len(numbers)

def median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]

def mode(numbers):
    from collections import Counter
    freq = Counter(numbers)
    max_count = max(freq.values())
    modes = [key for key, count in freq.items() if count == max_count]
    return modes if len(modes) > 1 else modes[0]

def standard_deviation(numbers):
    from math import sqrt
    mean_value = mean(numbers)
    return sqrt(sum((x - mean_value) ** 2 for x in numbers) / len(numbers))

# Trigonometric Functions
import math

def sine(angle):
    return math.sin(math.radians(angle))

def cosine(angle):
    return math.cos(math.radians(angle))

def tangent(angle):
    return math.tan(math.radians(angle))

def cotangent(angle):
    return 1 / tangent(angle)

def secant(angle):
    return 1 / cosine(angle)

def cosecant(angle):
    return 1 / sine(angle)

# Logarithmic Functions
def natural_log(num):
    return math.log(num)

def log_base_10(num):
    return math.log10(num)

def log_base_n(num, base):
    return math.log(num, base)

# Exponential Functions
def exponential(num):
    return math.exp(num)

def factorial(num):
    if num < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(num)

# Miscellaneous Functions
def is_even(num):
    return num % 2 == 0

def is_odd(num):
    return num % 2 != 0

def gcd(num1, num2):
    return math.gcd(num1, num2)

def lcm(num1, num2):
    return abs(num1 * num2) // gcd(num1, num2)

def square_root(num):
    return math.sqrt(num)

def cube_root(num):
    return num ** (1/3)
# Logical and Bitwise Operations
def logical_and(a, b): return a and b

def logical_or(a, b): return a or b

def logical_not(a): return not a

def bitwise_and(num1, num2): return num1 & num2

def bitwise_or(num1, num2): return num1 | num2

def bitwise_xor(num1, num2): return num1 ^ num2

def bitwise_not(num): return ~num

def left_shift(num, shifts): return num << shifts

def right_shift(num, shifts): return num >> shifts

# Relational Operations
def is_greater(num1, num2): return num1 > num2

def is_less(num1, num2): return num1 < num2

def is_equal(num1, num2): return num1 == num2

def is_not_equal(num1, num2): return num1 != num2

def is_greater_or_equal(num1, num2): return num1 >= num2

def is_less_or_equal(num1, num2): return num1 <= num2

def sum_list(numbers): 
    result = 0
    for num in numbers:
        result += num
    return result
def product_list(numbers): 
    result = 1
    for num in numbers:
        result *= num
    return result
def find_max(numbers): 
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
def find_min(numbers): 
    min_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
    return min_num
def count_occurrences(numbers, target): 
    count = 0
    for num in numbers:
        if num == target:
            count += 1
    return count

# Miscellaneous Operations
def factorial(num): 
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result
def gcd(num1, num2): 
    while num2:
        num1, num2 = num2, num1 % num2
    return num1
def lcm(num1, num2): return abs(num1 * num2) // gcd(num1, num2)
def square_root(num): 
    guess = num / 2.0
    for _ in range(20):  # Iteratively refine the guess
        guess = (guess + num / guess) / 2
    return guess
def cube_root(num): 
    guess = num / 3.0
    for _ in range(20):  # Iteratively refine the guess
        guess = (2 * guess + num / (guess * guess)) / 3
    return guess

# Geometric Operations
def area_of_circle(radius): 
    pi = 22 / 7
    return pi * (radius ** 2)
def circumference_of_circle(radius): 
    pi = 22 / 7
    return 2 * pi * radius
def area_of_rectangle(length, breadth): return length * breadth

def perimeter_of_rectangle(length, breadth): return 2 * (length + breadth)

def area_of_triangle(base, height): return 0.5 * base * height

def perimeter_of_triangle(a, b, c): return a + b + c

def area_of_square(side): return side ** 2

def perimeter_of_square(side): return 4 * side

def area_of_parallelogram(base, height): return base * height

def area_of_trapezium(a, b, height): return 0.5 * (a + b) * height

# Number Properties
def is_even(num): return num % 2 == 0
def is_odd(num): return num % 2 != 0
def is_prime(num): 
    if num < 2: return False
    for i in range(2, num):
        if num % i == 0: return False
    return True
def sum_of_digits(num): 
    total = 0
    while num:
        total += num % 10
        num //= 10
    return total
def reverse_number(num): 
    reversed_num = 0
    while num:
        reversed_num = reversed_num * 10 + num % 10
        num //= 10
    return reversed_num
def count_digits(num): 
    count = 0
    while num:
        count += 1
        num //= 10
    return count