import csv
import numpy as np
import time
import os
import multiprocessing
from multiprocessing import Manager

from AntColony import *
from BnBDFS import TSP_BnB_DFS


# Function for distance matrix reading
def read_distance_matrix_per_file(file_path):
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

# Function for saving results
def save_result(csv_file_path, algorithm_types, results):

    group_id = ["30"]
    uci_student_id = ["94086733", "29264828"]
    # results = [
    #     {"tour_length": 10, "cpu_time": 123.45}, 
    # ]

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(group_id)
        writer.writerow(uci_student_id)
        writer.writerow([algorithm_types])

        for result in results:
            writer.writerow([result["tour_length"], result["cpu_time"]])

    print(f"CSV file '{csv_file_path}' created successfully.")

# Function for AntColony Algorithm
def run_ant_colony(file_path, result_queue):
    print(f"loading file {file_path}...")
    print("start AntColony Algorithm...")
    n, distance_matrix = read_distance_matrix_per_file(file_path)
    
    num_ants = 10
    num_iterations = 100
    decay = 0.1

    ant_colony_start_time = time.time()
    best_path, best_cost = ant_colony(distance_matrix, num_ants, num_iterations, decay)
    ant_colony_end_time = time.time()
    ant_colony_runtime = ant_colony_end_time - ant_colony_start_time
    
    SLS_one_result =  {"tour_length":best_cost , "cpu_time": ant_colony_runtime}

    result_queue.put(SLS_one_result)

def run_ant_colony_parallel(file_folder, SLS_file_name):
    
    file_paths = [os.path.join(file_folder, file_name) for file_name in os.listdir(file_folder) if file_name.endswith(".txt")]

    # shared queue
    with Manager() as manager:
        result_queue = manager.Queue()

        with multiprocessing.Pool() as pool:
            
            pool.starmap(run_ant_colony, [(file_path, result_queue) for file_path in file_paths])

        results = []
        while not result_queue.empty():
            result = result_queue.get()
            results.append(result)

    # save file
    save_result(SLS_file_name, "SLS", results=results)


# Function for runing BnB Algorithm
def run_BnB(file_path, result_queue):
    print(f"loading file {file_path}...")
    print("start BnB DFS Algorithm...")

    n, distance_matrix = read_distance_matrix_per_file(file_path)

    t = TSP_BnB_DFS(n, distance_matrix)
    bnb_start_time = time.time()
    _, best_cost = t.BnB_DFS()
    bnb_end_time = time.time()
    bnb_runtime = bnb_end_time - bnb_start_time
    BnB_one_result =  {"tour_length":best_cost , "cpu_time": bnb_runtime}
    
    result_queue.put(BnB_one_result)

def run_BnB_parallel(file_folder, BnB_file_name):
    
    file_paths = [os.path.join(file_folder, file_name) for file_name in os.listdir(file_folder) if file_name.endswith(".txt")]

    # shared queue
    with Manager() as manager:
        result_queue = manager.Queue()

        with multiprocessing.Pool() as pool:
            
            pool.starmap(run_BnB, [(file_path, result_queue) for file_path in file_paths])

        results = []
        while not result_queue.empty():
            result = result_queue.get()
            results.append(result)

    # save file
    save_result(BnB_file_name,"BnB",results=results)


if __name__ == "__main__":

    RUN_ANTCOLONY = True
    RUN_BNB = True

    note = "-20-2"
    SLS_file_name = "SLS_result"+note+".csv"
    BnB_file_name = "BnB_result"+note+".csv"

    folder_path =  r"/Users/zhiyantan/Documents/UCI-MDS/271P/project/test_case_3"
    if RUN_ANTCOLONY:
        run_ant_colony_parallel(folder_path, SLS_file_name)
    if RUN_BNB:
        run_BnB_parallel(folder_path, BnB_file_name)

