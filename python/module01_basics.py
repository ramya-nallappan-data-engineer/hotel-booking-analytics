"""
=========================================================
Python Interview Lab
Module 01 - Python Fundamentals

Topics

Variables
Strings
Lists
Tuples
Sets
Dictionary
Loops
Functions
List Comprehension
=========================================================
"""
from numpy.ma.extras import average

"""Section A — Variables & Data Types"""

"""
Create variables for:

Your name
Years of experience
Current company

Print them in a readable sentence.
"""
my_name = "Ramya"
my_years_of_experience = 10
current_company = "Hexaware Technologies"


"""Find the data type of each variable"""
print(type(my_name))
print(type(my_years_of_experience))
print(type(current_company))

"""Swap two variables without using a third variable"""
a = 10
b = 20
a, b = b, a
print(a)
print(b)

"""Section B — Strings"""
"""
given:
company = "Agoda"
Print

First character
Last character
First three characters
Reverse string
"""
company = "Agoda"

print(company[0])
print(company[-1])
print(company[:3])
print(company[::-1])

"""
Count how many times the letter a appears in word "Data Engineering"
"""
word = "Data Engineering"
count_of_a = 0
for i in word:
    if i == "a":
        count_of_a += 1
print(count_of_a)

"""
Check whether a string is a palindrome
madam
level
racecar
"""
def is_palindrome(string):
    reverse_of_string = string[::-1]
    if string == reverse_of_string:
        return True
    else:
        return False
print(is_palindrome("madam"))
print(is_palindrome("level"))
print(is_palindrome("racecar"))

"""
Reverse every word individually.
Lead Data Engineer
"""
string_of_words = "Lead Data Engineer"
reversed_word = " ".join(word[::-1] for word in string_of_words.split())
print(f"reversed word is: {reversed_word}")

"""
Section C — Lists
"""
"""
Print

Largest
Smallest
Sum
Average
"""

numbers = [4, 8, 15, 16, 23, 42]
print(max(numbers))
print(min(numbers))
print(sum(numbers))
print(average(numbers))

"""Remove duplicates while preserving order"""
list_with_duplicates = [1,2,2,3,1,4,4,5]
new_list_without_duplicates = []
for i in list_with_duplicates:
    if i not in new_list_without_duplicates:
        new_list_without_duplicates.append(i)
print(new_list_without_duplicates)

"""Find the second largest number"""
numbers = [4, 8, 15, 16, 23, 42]
unique_numbers = list(set(numbers)) #to remove duplicates if any
unique_numbers.sort() #sort the list
if len(unique_numbers) >= 2:
    second_larget_number = unique_numbers[-2] #fetch the second number from the last
    print(f"second largest number is: {second_larget_number}")
else:
    print("No Second largest number")

"""Separate even and odd numbers"""
numbers = [4, 8, 15, 16, 23, 42]
even_list = []
odd_list = []
for i in numbers:
    if (i%2) == 0:
        even_list.append(i)
    else:
        odd_list.append(i)
print(f"even list: {even_list}")
print(f"odd list: {odd_list}")

"""Square every number using list comprehension"""
numbers = [4, 8, 15, 16, 23, 42]
square_of_numbers = []
for i in numbers:
    square_of_numbers.append(i*i)
print(square_of_numbers)

"""Section D — Dictionary"""
"""Create a dictionary representing a hotel."""
dictionary_of_hotel = {
    "hotel_name": "Grand Hotel Bengaluru",
    "city": "Bengaluru",
    "country": "India",
    "star_rating": 4.5
}
print(dictionary_of_hotel)

"""
Find the customer who spent the maximum amount.

Given

customers = {
    "Ram":3200,
    "John":2100,
    "Sara":5400,
    "Amit":4100
}
"""
customers = {
    "Ram":3200,
    "John":2100,
    "Sara":5400,
    "Amit":4100
}

customer_spent_max, customers_spent_value = max(customers.items(), key=lambda item: item[1])
print(f"customer who spent maximum is: {customer_spent_max} and the amount spent is: {customers_spent_value}")

"""Merge two dictionaries."""
merged_of_dictionaries = dictionary_of_hotel | customers
print(f"merge of two dictionaries is: {merged_of_dictionaries}")

"""Section E — Loops"""
"""Print numbers from 1 to 20"""
num = 20
for i in range(1,num+1):
    print(i)
    """Print only multiples of 3"""
    if (i%3) == 0:
        print(f"multiples of 3: {i}")
    if (i%7) == 0:
        print(f"multiples of 7: {i}")

"""print a pyramid"""


"""Count vowels in a string."""
vowels = ['a', 'e', 'i', 'o', 'u']
string = "Ramya"
vowels_in_string = []
for letter in string:
    if letter in vowels:
        vowels_in_string.append(letter)
print(vowels_in_string)

"""Section F — Functions"""
"""Write a function to calculate factorial."""
def calculate_factorial(number):
    factorial = 1
    for i in range(1, number+1):
        factorial *= i
    return factorial
print(f"factorial of number is: {calculate_factorial(5)}")

"""Write a function to check whether a number is prime."""
def is_prime(number):
    if number == 2 and (number%2):
        return True
    elif number != 2 and (number%number) == 0 and (number%2) != 0:
        return True
    else:
        return False
print(f"Is the given number Prime? {is_prime(3)}")

"""Write a function to find the largest of three numbers."""
def largest_of_three_numbers(list_of_num):
    highest_of_three = list_of_num[0]
    for i in range(1, len(list_of_num)+1):
        if i > highest_of_three:
            highest_of_three = i
            i += 1
    return highest_of_three
print(f"largest of three numbers is: {largest_of_three_numbers([2,3,5])}")

"""
Write a function to calculate booking discount.
Inputs

Amount

Discount %

Return the final amount.
"""
def calculate_booking_discount(amount, discount_percent):
    final_amount = amount - (amount * (discount_percent/100))
    return final_amount
print(f"Final amount after disocunt is: {calculate_booking_discount(100, 10)}")

"""
Question 25 ⭐ Interview Favorite

Given a list

bookings = [
    {"customer":"Ram","amount":1200},
    {"customer":"Sara","amount":1800},
    {"customer":"John","amount":900},
]

Return the customer with the highest booking amount.
"""
bookings = [
    {"customer":"Ram","amount":1200},
    {"customer":"Sara","amount":1800},
    {"customer":"John","amount":900},
]


#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'fizzBuzz' function below.
#
# The function accepts INTEGER n as parameter.
#

def fizzBuzz(n):
    # Write your code here
    for i in range(1, n+1):
        if (i%3)==0 and (i%5)==0:
            return 'FizzBuzz'
        elif (i%3):
            return 'Fizz'
        elif (i%5):
            return 'Buzz'
        else:
            return i

if __name__ == '__main__':
    n = int(input().strip())

    print(fizzBuzz(15))
