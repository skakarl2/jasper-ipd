# Sample list of numbers
numbers = [5, 2, 9, 1, 5, 6]

# Sort the list in ascending order
sorted_numbers = sorted(numbers)
print("Sorted in ascending order:", sorted_numbers)

# Sort the list in descending order
sorted_numbers_desc = sorted(numbers, reverse=True)
print("Sorted in descending order:", sorted_numbers_desc)

# Sample list of dictionaries
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 20}
]

# Sort the list of dictionaries by age
sorted_people = sorted(people, key=lambda person: person["age"])
print("Sorted by age:", sorted_people)

# Sort the list of dictionaries by name
sorted_people_by_name = sorted(people, key=lambda person: person["name"])
print("Sorted by name:", sorted_people_by_name)

# Sort the list of dictionaries by the length of the name# Sort the list of dictionaries by the length of the name




print("Sorted by name length:", sorted_people_by_name_length)sorted_people_by_name_length = sorted(people, key=lambda person: len(person["name"]))sorted_people_by_name_length = sorted(people, key=lambda person: len(person["name"]))
print("Sorted by name length:", sorted_people_by_name_length)

