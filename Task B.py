import pandas as pd
from collections import defaultdict
from itertools import combinations
from scipy.cluster.hierarchy import linkage, fcluster
import numpy as np

# --- Step 1: Define the Orders ---

# Orders are defined as a dictionary where the key is the order number and the value is a list of articles
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

# Convert to a DataFrame for easier handling
article_frequency = pd.DataFrame.from_dict(article_counts, orient='index', columns=['Frequency'])
article_frequency.index.name = 'Article'
article_frequency.reset_index(inplace=True)

# Display Access Frequencies
print("Access Frequencies:")
print(article_frequency.sort_values(by='Article'))
print("\n")

# --- Step 3: Scenario A - Assign Articles in Ascending Order ---

# Assign positions from 1 to 10 in ascending order
scenario_a_positions = {article: position for position, article in enumerate(sorted(article_counts.keys()), start=1)}

# --- Step 4: Scenario B - Assign Articles in Descending Access Frequency ---

# Sort articles by frequency in descending order
sorted_articles_by_frequency = article_frequency.sort_values(by='Frequency', ascending=False)
scenario_b_positions = {article: position for position, article in enumerate(sorted_articles_by_frequency['Article'], start=1)}

# --- Step 5: Scenario C - Clustering Based on Common Removals ---

# Calculate common removals for each pair of articles
pair_common_removals = defaultdict(int)

for order_items in orders.values():
    for article_pair in combinations(sorted(set(order_items)), 2):
        pair_common_removals[article_pair] += 1

# Create a DataFrame from pair_common_removals
pairs = []
for (article1, article2), count in pair_common_removals.items():
    pairs.append({'Article1': article1, 'Article2': article2, 'CommonRemovals': count})
pair_common_removals_df = pd.DataFrame(pairs)

# Create a distance matrix
articles = sorted(article_counts.keys())
article_index = {article: idx for idx, article in enumerate(articles)}
num_articles = len(articles)
distance_matrix = np.full((num_articles, num_articles), fill_value=50, dtype=float)  # Initialize with maximum distance

for _, row in pair_common_removals_df.iterrows():
    i = article_index[row['Article1']]
    j = article_index[row['Article2']]
    # Distance is defined as 50 - common removals
    distance = 50 - row['CommonRemovals']
    distance_matrix[i, j] = distance
    distance_matrix[j, i] = distance  # Symmetric matrix

# Perform hierarchical clustering using average linkage
linkage_matrix = linkage(distance_matrix, method='average')

# Form clusters with a distance threshold of <7
cluster_assignments = fcluster(linkage_matrix, t=7, criterion='distance')

# Group articles into clusters
clusters = defaultdict(list)
for article, cluster_id in zip(articles, cluster_assignments):
    clusters[cluster_id].append(article)

# Calculate total access numbers for each cluster
cluster_access_numbers = {}
for cluster_id, cluster_articles in clusters.items():
    total_access = sum(article_counts[article] for article in cluster_articles)
    cluster_access_numbers[cluster_id] = total_access

# Sort clusters by descending total access numbers
sorted_clusters = sorted(clusters.items(), key=lambda item: cluster_access_numbers[item[0]], reverse=True)

# Arrange articles within clusters by descending access numbers
scenario_c_positions = {}
position_counter = 1
for cluster_id, cluster_articles in sorted_clusters:
    # Sort articles within the cluster by descending frequency
    sorted_articles = sorted(cluster_articles, key=lambda article: article_counts[article], reverse=True)
    for article in sorted_articles:
        scenario_c_positions[article] = position_counter
        position_counter += 1

# --- Step 6: Calculate Picking Routes for Each Scenario ---

def calculate_total_distance(positions_dict):
    total_distance = 0
    for order_num, order_items in orders.items():
        # Get the positions of the articles in the order
        pick_positions = [positions_dict[article] for article in order_items]
        # Sort the pick positions to determine the optimal path (ascending order)
        sorted_positions = sorted(pick_positions)
        # Calculate distance
        if not sorted_positions:
            continue  # Skip if no items in order
        distance = sorted_positions[0]  # From base to first pick
        for i in range(1, len(sorted_positions)):
            distance += sorted_positions[i] - sorted_positions[i - 1]  # Between picks
        distance += sorted_positions[-1]  # From last pick back to base
        total_distance += distance
    return total_distance

# Calculate total distances for each scenario
total_distance_a = calculate_total_distance(scenario_a_positions)
total_distance_b = calculate_total_distance(scenario_b_positions)
total_distance_c = calculate_total_distance(scenario_c_positions)

# --- Step 7: Output the Results ---

print("Total Picking Distance for Scenario A (Ascending Order): {} meters".format(total_distance_a))
print("Total Picking Distance for Scenario B (Descending Access Frequency): {} meters".format(total_distance_b))
print("Total Picking Distance for Scenario C (Clustering): {} meters".format(total_distance_c))

print("\nScenario A Positions (Ascending Order):")
print(sorted(scenario_a_positions.items(), key=lambda x: x[1]))

print("\nScenario B Positions (Descending Access Frequency):")
print(sorted(scenario_b_positions.items(), key=lambda x: x[1]))

print("\nScenario C Positions (Clustering):")
print(sorted(scenario_c_positions.items(), key=lambda x: x[1]))
