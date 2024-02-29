# Travelling Salesman Problem
# use AntColony algorithm
import numpy as np
import random


# Function to generate a random distance matrix
def generate_distance_matrix(n, mean, sigma):
    distance_matrix = np.zeros((n, n))
    random_distance = []
    num_distance = int(n * (n-1) / 2)
    for _ in range(num_distance):
        distance = 0
        while distance <= 0:
            distance = np.random.normal(mean, sigma)
        random_distance.append(distance)

    iu = np.triu_indices(n, 1)
    distance_matrix[iu] = random_distance
    distance_matrix += distance_matrix.T
    return distance_matrix

# Function for distance matrix reading
def read_distance_matrix(file_path):
    try:
        with open(file_path, 'r') as file:
            n = int(file.readline().strip())
            distance_matrix = np.loadtxt(file, delimiter=None)
            return n, distance_matrix
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
    

# Function to calculate the total distance of a path
def calculate_total_distance(path, distance_matrix):
    total_distance = sum(distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))
    total_distance += distance_matrix[path[-1]][path[0]]
    return total_distance


# Initialize pheromone matrix
def initialize_pheromone_matrix(num_cities):
    return np.ones((num_cities, num_cities))


# Calculate probabilities for each city
def calculate_probabilities(pheromone_matrix, distance_matrix, current_city, visited_cities, alpha, beta):
    probabilities = []
    denominator = 0
    for city in range(len(pheromone_matrix)):
        if city not in visited_cities:
            pheromone = pheromone_matrix[current_city][city]
            distance = 1/(distance_matrix[current_city][city] if distance_matrix[current_city][city]>0 else 1)
            probabilities.append((city, pheromone ** alpha * distance ** beta))
            denominator += pheromone ** alpha * distance ** beta
    # item[0]->city index, item[1]->probability
    return [(item[0], item[1]/denominator) for item in probabilities if denominator > 0]


# Select the next city based on probabilities with roulette wheel
def roulette_wheel_selection(probabilities):
    r = random.uniform(0, 1)
    current = 0
    for choice, probability in probabilities:
        current += probability
        if current > r:
            return choice


# Update the pheromone matrix
def update_pheromone(pheromone_matrix, ant_paths, distance_matrix, decay):
    pheromone_matrix *= (1-decay)
    for ant_path in ant_paths:
        total_distance = calculate_total_distance(ant_path, distance_matrix)
        pheromone_to_deposit = 1/total_distance
        for i in range(len(ant_path)-1):
            pheromone_matrix[ant_path[i]][ant_path[i+1]] += pheromone_to_deposit
        pheromone_matrix[ant_path[-1]][ant_path[0]] += pheromone_to_deposit
    return pheromone_matrix


# Find the best path
def find_best_path(ant_paths, distance_matrix):
    # using lambda function to compare the paths based on their total distances
    best_path = min(ant_paths, key=lambda path: calculate_total_distance(path, distance_matrix))
    return best_path


# Ant Colony Optimization algorithm
def ant_colony(distance_matrix, num_ants, num_iterations, decay, alpha=1, beta=2):
    random.seed(42)
    num_cities = len(distance_matrix)
    pheromone_matrix = initialize_pheromone_matrix(num_cities)

    for iteration in range(num_iterations):
        ant_paths = []
        for ant in range(num_ants):
            start_city = random.choice(range(num_cities))
            current_city = start_city
            ant_path = [current_city]
            visited_cities = set([current_city])
            for i in range(1, num_cities):
                probabilities = calculate_probabilities(
                    pheromone_matrix, distance_matrix, current_city, visited_cities, alpha, beta)
                selected_city = roulette_wheel_selection(probabilities)
                ant_path.append(selected_city)
                current_city = selected_city
                visited_cities.add(current_city)

            # ensure return to the starting city
            ant_path.append(start_city)
            # add the complete path
            ant_paths.append(ant_path)

        pheromone_matrix = update_pheromone(pheromone_matrix, ant_paths, distance_matrix, decay)

    best_path = find_best_path(ant_paths, distance_matrix)
    best_cost = calculate_total_distance(best_path, distance_matrix)
    return best_path, best_cost


if __name__ == "__main__":
    n = int(input("Enter the number of locations: "))
    mean = float(input("Enter the mean distance: "))
    sigma = float(input("Enter the standard deviation: "))

    distance_matrix = generate_distance_matrix(n, mean, sigma)
    print("Generated distance matrix:")
    print(distance_matrix)

    num_ants = 10
    num_iterations = 100
    decay = 0.1
    best_path, best_cost = ant_colony(distance_matrix, num_ants, num_iterations, decay)
    print("Best path:", best_path)
    print("Best cost:", best_cost)
