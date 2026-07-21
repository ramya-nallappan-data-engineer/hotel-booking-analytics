"""List comprehensions"""
"""Create a list of their cubes."""
numbers = [2, 4, 6, 8, 10]
result = [i ** i for i in numbers]
print(result)

"""Convert every name to uppercase."""
names = ["ramya", "haresh", "arya"]
upper_of_names = [i.upper() for i in names]
print(upper_of_names)

"""Create a list containing only odd numbers."""
numbers = list(range(1, 21))
odd_list = [num for num in numbers if num % 2 == 1]
print(odd_list)

"""Create a list containing the length of each word."""
words = ["Snowflake", "Azure", "Python", "SQL"]
length_of_words = [len(word) for word in words]
print(length_of_words)

"""Increase every price by 18% GST."""
prices = [1200, 800, 2500, 4000]
gst_price = [price + price * 0.18 for price in prices]
print(gst_price)

"""Using one list comprehension, remove all empty strings."""
words = ["SQL", "", "Python", "", "Snowflake", ""]
non_empty_strings = [word for word in words if word]
print(non_empty_strings)