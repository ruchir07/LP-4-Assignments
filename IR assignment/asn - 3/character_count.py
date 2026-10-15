from collections import defaultdict


def mapper(text):
    # Emit (character, 1) for every alphabetic character
    for char in text.lower():
        if char.isalpha() and char.isascii():
            yield (char, 1)


def reducer(mapped_data):
    # Group values by character
    grouped = defaultdict(list)

    for char, count in mapped_data:
        grouped[char].append(count)

    # Add the values for each character
    result = {}

    for char, counts in grouped.items():
        result[char] = sum(counts)

    return result


# Input dataset
dataset = """
Hello World!
MapReduce is useful.
HELLO
"""

# Map phase
mapped_data = list(mapper(dataset))

print("===== MAP OUTPUT =====")
print(mapped_data)

# Reduce phase
result = reducer(mapped_data)

print("\n===== CHARACTER COUNTS =====")
for char in sorted(result):
    print(f"{char}: {result[char]}")