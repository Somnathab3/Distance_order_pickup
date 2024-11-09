import pandas as pd
from collections import defaultdict
import random

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

# Convert to a DataFrame for easier handling
article_frequency = pd.DataFrame.from_dict(article_counts, orient='index', columns=['Frequency'])
article_frequency.index.name = 'Article'
article_frequency.reset_index(inplace=True)

# Display Access Frequencies
print("=== Access Frequencies ===")
print(article_frequency.sort_values(by='Article'))
print("\n")

# --- Identify Articles with Duplicate Frequencies ---

frequency_groups = article_frequency.groupby('Frequency')['Article'].apply(list).to_dict()
duplicate_frequencies = {freq: articles for freq, articles in frequency_groups.items() if len(articles) > 1}

print("=== Articles with Duplicate Frequencies ===")
for freq, articles_dup in duplicate_frequencies.items():
    print(f"Frequency {freq}: Articles {articles_dup}")
print("\n")

# --- Step 3: Implementing the Genetic Algorithm for Optimization ---

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.7
ELITISM = True

# Function to calculate total picking distance for GA
def calculate_total_distance_ga(assignment):
    total_distance = 0
    for order_num, order_items in orders.items():
        # Get the positions of the articles in the order
        pick_positions = [assignment[article] for article in order_items]
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

# Initialize population with random assignments
def initialize_population(articles, positions, population_size):
    population = []
    for _ in range(population_size):
        shuffled_positions = positions.copy()
        random.shuffle(shuffled_positions)
        individual = dict(zip(articles, shuffled_positions))
        population.append(individual)
    return population

# Tournament selection
def tournament_selection(population, scores, k=3):
    selection_ix = random.randint(0, len(population)-1)
    for ix in random.sample(range(len(population)), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return population[selection_ix]

# Crossover two parents to create two children
def crossover(parent1, parent2):
    # Order Crossover (OX) Implementation
    child1 = {}
    child2 = {}
    
    # Choose two crossover points
    start, end = sorted(random.sample(range(len(parent1)), 2))
    
    # Extract the subset from parent1 and parent2
    subset1 = list(parent1.keys())[start:end]
    subset2 = list(parent2.keys())[start:end]
    
    # Initialize children with subsets
    child1 = {k: parent1[k] for k in subset1}
    child2 = {k: parent2[k] for k in subset2}
    
    # Fill the remaining genes
    def fill_child(child, parent, subset):
        for article in parent.keys():
            if article not in subset:
                # Find the first available position
                for pos in sorted(parent.values()):
                    if pos not in child.values():
                        child[article] = pos
                        break
        return child
    
    child1 = fill_child(child1, parent2, subset1)
    child2 = fill_child(child2, parent1, subset2)
    
    return child1, child2

# Mutation: Swap two articles' positions
def mutate(individual, mutation_rate):
    articles = list(individual.keys())
    for article in articles:
        if random.random() < mutation_rate:
            article2 = random.choice(articles)
            # Swap positions
            individual[article], individual[article2] = individual[article2], individual[article]
    return individual

# Genetic Algorithm main function
def genetic_algorithm(articles, positions, population_size, generations, mutation_rate, crossover_rate, elitism=True):
    # Initialize population
    population = initialize_population(articles, positions, population_size)
    
    # Evaluate initial population
    scores = [calculate_total_distance_ga(ind) for ind in population]
    
    # Track the best solution
    best_score = min(scores)
    best_individual = population[scores.index(best_score)]
    
    for gen in range(generations):
        # Select the next generation
        next_generation = []
        
        # Elitism: carry forward the best individual
        if elitism:
            next_generation.append(best_individual)
        
        # Generate new individuals
        while len(next_generation) < population_size:
            # Selection
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            
            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            # Add to next generation
            next_generation.extend([child1, child2])
        
        # Trim the population to the desired size
        population = next_generation[:population_size]
        
        # Evaluate the new population
        scores = [calculate_total_distance_ga(ind) for ind in population]
        
        # Update the best solution found
        min_score = min(scores)
        if min_score < best_score:
            best_score = min_score
            best_individual = population[scores.index(min_score)]
        
        # Optional: Print progress
        if (gen+1) % 50 == 0 or gen == 0:
            print(f"Generation {gen+1}: Best Distance = {best_score} meters")
    
    return best_individual, best_score

# --- Step 4: Run the Genetic Algorithm ---

# Parameters
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.7

# Define articles and positions
articles = list(article_counts.keys())
positions = list(range(1, len(articles) + 1))

# Run GA
best_assignment_ga, best_distance_ga = genetic_algorithm(
    articles=articles,
    positions=positions,
    population_size=POPULATION_SIZE,
    generations=GENERATIONS,
    mutation_rate=MUTATION_RATE,
    crossover_rate=CROSSOVER_RATE,
    elitism=True
)

print("=== Optimal Assignment (Genetic Algorithm) ===")
for article, position in sorted(best_assignment_ga.items(), key=lambda x: x[1]):
    print(f"Article {article}: Position {position}")
print("\n")

print(f"Total Picking Distance (Genetic Algorithm): {best_distance_ga} meters")
print("\n")
