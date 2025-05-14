# Step-by-step beginner-style code for the Bincom ICT shirt color analysis interview

import re
import psycopg2
import random
from statistics import mean, median, variance
from collections import Counter

# Extracted data from the HTML page (manually collected from the table)
data = {
    "Monday": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "Tuesday": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "Wednesday": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "Thursday": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "Friday": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
}

# Step 1: Clean and normalize colour data
all_colours = []
for day in data:
    colours = data[day].upper().replace("BLEW", "BLUE").replace("ARSH", "ASH")
    all_colours += [color.strip() for color in colours.split(',')]

# Count frequency of each colour
colour_counts = Counter(all_colours)

# 1. Mean color (color with average frequency rounded to nearest)
avg_freq = round(mean(colour_counts.values()))
mean_colour = [color for color, count in colour_counts.items() if count == avg_freq]

# 2. Most worn color
most_common_colour = colour_counts.most_common(1)[0][0]

# 3. Median color (get color(s) with median frequency)
med = median(colour_counts.values())
median_colour = [color for color, count in colour_counts.items() if count == med]

# 4. Variance of color frequencies
var = variance(colour_counts.values())

# 5. Probability of choosing red
total_colours = len(all_colours)
red_count = colour_counts['RED'] if 'RED' in colour_counts else 0
prob_red = red_count / total_colours

# 6. Save to PostgreSQL database (assuming PostgreSQL is running locally with a test database)
def save_to_db(data_dict):
    try:
        conn = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="yourpassword",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS colour_frequency")
        cur.execute("CREATE TABLE colour_frequency (colour TEXT, frequency INT)")
        for colour, freq in data_dict.items():
            cur.execute("INSERT INTO colour_frequency (colour, frequency) VALUES (%s, %s)", (colour, freq))
        conn.commit()
        cur.close()
        conn.close()
        print("Data saved to database successfully.")
    except Exception as e:
        print("Database error:", e)

# 7. Recursive search algorithm
def recursive_search(arr, target, index=0):
    if index >= len(arr):
        return -1
    if arr[index] == target:
        return index
    return recursive_search(arr, target, index + 1)

# 8. Random binary to decimal converter
def binary_to_decimal():
    binary = ''.join(random.choice('01') for _ in range(4))
    decimal = int(binary, 2)
    return binary, decimal

# 9. Sum first 50 Fibonacci numbers
def sum_fibonacci(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Show outputs
print("Mean Colour:", mean_colour)
print("Most Worn Colour:", most_common_colour)
print("Median Colour:", median_colour)
print("Variance:", var)
print("Probability of Red:", prob_red)

# Save to DB
# Uncomment below when database is set up correctly
# save_to_db(colour_counts)

# Test recursive search
numbers = [10, 20, 30, 40, 50]
search_num = 30
print("Search Result:", recursive_search(numbers, search_num))

# Test binary to decimal
binary, decimal = binary_to_decimal()
print(f"Binary: {binary}, Decimal: {decimal}")

# Fibonacci sum
print("Sum of first 50 Fibonacci numbers:", sum_fibonacci(50))
