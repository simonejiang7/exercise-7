import numpy as np

from environment import Environment
from ant import Ant 

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:

    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, self.ant_population)
        # Get the pheromone matrix of the environment
        self.pheromone_matrix = self.environment.initialize_pheromone_map()

        # Initilize the list of ants of the ant colony
        self.ants = []
        # Initialize the sum of pheromone of zero values
        self.sum_pheromone = np.zeros((self.environment.get_num_locations(), self.environment.get_num_locations()))

    # Solve the ant colony optimization problem  
    def solve(self):

        iter = 0
        shortest_distance = np.inf

        while iter < self.iterations:

            print("=> iteration: ", iter+1)

            i = 0

            for i in range(self.ant_population):

                print("=> ant: ", i+1)

                # Randomly select an initial location for the ant
                initial_location = np.random.randint(0, self.environment.get_num_locations())
                print("=> initial_location: ", initial_location)
                
                # Initialize an ant
                ant = Ant(self.alpha, self.beta, initial_location)
                ant.join(self.environment)

                # Make the ant move and traverse the environment
                ant.run()

                # Calculate the ant's travelled distance, sum of travelled distance and visited locations
                ant_travel_distance, sum_distance = ant.get_travelled_distance()
                ant_visited_locations = ant.get_visited_location()

                print("=> ant travel distance: ", ant_travel_distance)
                print("=> ant sum distance: ", sum_distance)
                print("=> ant visited locations: ", ant_visited_locations)
                print("=> ant final location: ", ant_visited_locations[-1])

                # Update the shortest distance and the solution if the ant's travelled distance is less than the shortest distance
                if sum_distance < shortest_distance:
                    shortest_distance = sum_distance
                    solution = ant_visited_locations

                for i in range(len(ant_visited_locations)-1):
                    location = ant_visited_locations[i]
                    # print("debug location: ", location)
                    next_location = ant_visited_locations[i+1]
                    # print("debug next_location: ", next_location)
                    self.sum_pheromone[location][next_location] += 1 / ant_travel_distance[i+1]
                    self.sum_pheromone[next_location][location] += 1 / ant_travel_distance[i+1]
                    # print("debug ant_travel_distance[i+1]: ", ant_travel_distance[i+1])

                # print("=> sum_pheromone: ", self.sum_pheromone[:10,])

                
                # Add the ant to the ant colony
                self.ants.append(ant)

                # i += 1
                # print("i: ", i)

            # self.environment.update_pheromone_matrix(self.sum_pheromone)

            iter += 1

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(ant_population = 5, iterations = 10, alpha = 2, beta = 5, rho = 0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    