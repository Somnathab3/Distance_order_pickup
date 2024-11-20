# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:56:12 2024

@author: somna
"""
import pandas as pd
from collections import defaultdict
from itertools import permutations

# --- Step 1: Define the Orders ---

orders = {
    1: [4, 7, 2, 5, 9],
    2: [6, 4, 8],
    3: [8, 5, 6, 9, 1],
    4: [7, 3, 8, 10, 4],
    5: [4, 9, 8],
    6: [8, 1, 2, 6],
    7: [7, 8, 5, 1],
    8: [5, 7, 6, 2, 9],
    9: [10, 6],
    10: [9, 2, 6, 1],
    11: [9, 5, 2],
    12: [10, 4],
    13: [6, 4, 3],
    14: [2, 3, 6],
    15: [7, 9],
    16: [2, 6, 4, 7],
    17: [6, 4],
    18: [1, 6, 4],
    19: [1, 8, 5],
    20: [4, 6, 8, 5, 7],
    21: [8, 4, 1, 9],
    22: [1, 7, 2],
    23: [6, 2, 7, 9, 5],
    24: [1, 8, 5],
    25: [8, 5],
    26: [1, 5],
    27: [4, 9, 8, 1],
    28: [7, 6, 3],
    29: [1, 7, 2],
    30: [1, 7, 6],
    31: [9, 7, 4, 3, 1],
    32: [6, 5, 8],
    33: [2, 1, 6, 9],
    34: [3, 9, 1],
    35: [5, 3],
    36: [8, 5, 6],
    37: [9, 7, 2, 6, 5],
    38: [9, 3, 4, 2],
    39: [7, 8, 6],
    40: [6, 9, 2],
    41: [9, 4, 6, 7, 5],
    42: [5, 9],
    43: [6, 9, 2],
    44: [7, 1, 8, 2, 3],
    45: [5, 1, 8],
    46: [8, 10, 7, 5, 3],
    47: [5, 7],
    48: [5, 9, 4],
    49: [1, 2, 6],
    50: [6, 9, 4, 1]
}

# --- Step 2: Calculate Access Frequencies ---

# Count the frequency of each article
article_counts = defaultdict(int)
for order_items in orders.values():
    for article in order_items:
        article_counts[article] += 1

# Print out the frequency of each article
print("=== Access Frequencies ===")
for article, count in sorted(article_counts.items()):
    print(f"Article {article}: Frequency {count}")
print("\n")

# Function to calculate total picking distance for a given assignment
def calculate_total_distance_ga(assignment):
    total_distance = 0
    for order_items in orders.values():
        pick_positions = [assignment[article] for article in order_items]
        pick_positions.sort()
        distance = pick_positions[0]
        for i in range(1, len(pick_positions)):
            distance += pick_positions[i] - pick_positions[i - 1]
        distance += pick_positions[-1]
        total_distance += distance
    return total_distance

# --- Brute Force to Find Optimal Assignment ---

def brute_force_min_distance(articles, positions):
    all_assignments = permutations(positions)
    min_distance = float('inf')
    best_assignment = None

    # Track progress
    count = 0
    for assignment in all_assignments:
        count += 1
        assignment_dict = dict(zip(articles, assignment))
        distance = calculate_total_distance_ga(assignment_dict)
        
        # Print each assignment and its distance for debugging
        print(f"Assignment {count}: {assignment_dict} => Total Distance: {distance} meters")

        if distance < min_distance:
            min_distance = distance
            best_assignment = assignment_dict

    return best_assignment, min_distance

# Define articles and positions
articles = list(article_counts.keys())
positions = list(range(1, len(articles) + 1))

# Run brute force
print("=== Running Brute Force ===")
best_assignment_bf, best_distance_bf = brute_force_min_distance(articles, positions)

# Display Results
print("\n=== Optimal Assignment (Brute Force) ===")
for article, position in sorted(best_assignment_bf.items(), key=lambda x: x[1]):
    print(f"Article {article}: Position {position}")
print("\n")
print(f"Total Picking Distance (Brute Force): {best_distance_bf} meters")
