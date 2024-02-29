# Travelling Salesman Problem
# use BnB DFS and SLS algorithm
import numpy as np
import random
import time


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

# Class to store a CityNode
class CityNode:
    def __init__(self, number:int, level:int, current_cost:int, rest_cost:int) -> None:
        
        self.number = number # index in intial map
        self.level = level # index in a search tree
 
        self.rest_cost = rest_cost 
        self.current_cost = current_cost
        self.lcost = current_cost + rest_cost   # lower bound
        self.x = []  # store the number of each node in the path
        

    def __lt__(self, other):
        return self.lcost < other.lcost


class TSP_BnB_DFS:
    
    def __init__(self, num_locations, distance_matrix) -> None:
        
        if num_locations < 2:
            raise ValueError("need at least two cities")
        self.n = num_locations
        self.distance_matrix = distance_matrix
        self.NoEdge = 0
        
        _ , self.best_cost = self.greedy_tsp()
        self.best_path = [] 
        self.total_cost = 0
        self.stack_for_searched_node = []
        
        self.min_out = [0] * self.n
        self.calculate_min_out()
        
        self.init_node = CityNode(1,0,0, sum(self.min_out))
        # number, level, current_cost, rest_cost
        self.init_node.x = list(range(self.n))
        for i in range(self.n):
            self.init_node.x[i] = i

        self.stack_for_searched_node.append(self.init_node)
        
    
    def calculate_min_out(self):
        for i in range(self.n):
            min_out = float('inf')
            for j in range(self.n):
                edge = self.distance_matrix[i][j]
                if edge != self.NoEdge:
                    if edge < min_out:
                        min_out = edge
            self.min_out[i] = min_out
        

    def greedy_tsp(self):
        visited = [False] * self.n
        current_city = 0
        # best path
        tour = [current_city]
        visited[current_city] = True
        total_distance = 0

        # choose the nearest city from current city
        for _ in range(self.n - 1):
            min_distance = float('inf')
            nearest_city = None

            for next_city in range(self.n):
                if not visited[next_city] and next_city != current_city:
                    distance = self.distance_matrix[current_city][next_city]
                    if distance < min_distance:
                        min_distance = distance
                        nearest_city = next_city

            # tag that current city has been visited
            visited[nearest_city] = True
            current_city = nearest_city
            tour.append(current_city)
            total_distance += min_distance

        # back to the init node
        total_distance += self.distance_matrix[tour[-1]][tour[0]]
        tour.append(tour[0])
        
        return tour, total_distance

    def BnB_DFS(self):

            while self.stack_for_searched_node:
                cur_node = self.stack_for_searched_node.pop()
                
                if cur_node.level == self.n - 1: # current node is a leaf node
                    if self.distance_matrix[cur_node.x[-1]][cur_node.x[0]] != self.NoEdge:  # check if there is a path back to the initial node
                        current_cost = cur_node.current_cost + self.distance_matrix[cur_node.x[-1]][cur_node.x[0]]
                        
                        if current_cost < self.best_cost:
                            self.best_cost = current_cost
                            self.best_path = cur_node.x + [cur_node.x[0]]
                else: # current node is not the leaf node
                    for i in range(cur_node.level + 1, self.n):
                        new_edge = self.distance_matrix[cur_node.x[cur_node.level]][cur_node.x[i]] 

                        if new_edge != self.NoEdge:
                            current_cost = cur_node.current_cost + new_edge
                            rest_cost = cur_node.rest_cost - self.min_out[cur_node.x[cur_node.level]]
                            # prune if L(n)>=H(n)
                            if current_cost + rest_cost < self.best_cost:
                                new_node = CityNode(cur_node.x[i], cur_node.level + 1, current_cost, rest_cost)
                                new_node.x = cur_node.x[:cur_node.level + 1] + cur_node.x[i:] + cur_node.x[cur_node.level + 1:i]
                                self.stack_for_searched_node.append(new_node)

            return self.best_path, self.best_cost



if __name__ == "__main__":
    file_path = r"generate_travelling_salesman_problem/5_0.0_10.0.out"
    n, distance_matrix = read_distance_matrix(file_path)
    print("n:", n)
    print("Generated distance matrix:")
    print(distance_matrix)

    
    t = TSP_BnB_DFS(n, distance_matrix)
    best_path, best_distance = t.BnB_DFS()
    print("BnB DFS")
    print("Best path:", best_path)
    print("Best cost:", best_distance)

    print("Greedy Search")
    tour, distance = t.greedy_tsp()
    print("Best path:", tour)
    print("Best cost:", distance)


   
