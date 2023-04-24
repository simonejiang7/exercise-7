import math
import tsplib95
import numpy as np

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho, ant_population):

        self.rho =rho
        self.ant_population = ant_population
        
        # Initialize the environment topology

        with open('att48-specs/att48.tsp') as f:
            problem = tsplib95.read(f)

        # Intialize the pheromone map in the environment
        print("=> initialize the pheromone map in the environment")
        # print(problem.as_name_dict())

        self.problem = problem
        self.node = list(problem.get_nodes())
        self.edge = list(problem.get_edges())
        self.node_coords = problem.node_coords
        self.node_count = len(problem.node_coords)
        self.edge_count = len(list(problem.get_edges()))
        self.possible_locations = list(range(self.node_count))

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self):

        distance_matrix = np.array([
            [
                tsplib95.distances.euclidean(self.node_coords[self.edge[i * self.node_count + j][0]], self.node_coords[self.edge[i * self.node_count + j][1]])
                for j in range(self.node_count)
            ]
            for i in range(self.node_count)
        ])

        pheromone_matrix = np.array([
            [
                self.ant_population / min(val for val in distance_matrix[j] if val != 0)
                for i in range(self.node_count)
            ]
            for j in range(self.node_count)
        ])

        np.fill_diagonal(pheromone_matrix, 0)

        self.distance_matrix = distance_matrix
        self.pheromone_matrix = pheromone_matrix

        return pheromone_matrix

    # Update the pheromone trails in the environment
    def update_pheromone_matrix(self, sum_pheromone):

        # negative feedback
        self.distance_matrix = self.distance_matrix * self.rho

        # positive feedback
        self.pheromone_matrix = self.pheromone_matrix + sum_pheromone

    # Get the pheromone trails in the environment
    def get_pheromone_matrix(self):
        return self.pheromone_matrix
    
    # Get the environment topology
    def get_possible_locations(self):
        return self.possible_locations
    
    def get_location_coords(self, location):
        return self.node_coords[location+1] # location range: 1-48
    
    def get_num_locations(self):
        return self.node_count

    
