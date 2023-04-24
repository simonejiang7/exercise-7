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
        self.pheromone_matrix = self.environment.initialize_pheromone_map()

        # Initilize the list of ants of the ant colony
        self.ants = []
        self.sum_pheromone = np.zeros((self.environment.get_num_locations(), self.environment.get_num_locations()))

    # Solve the ant colony optimization problem  
    def solve(self):

        iter = 0
        shortest_distance = np.inf

        while iter < self.iterations:

            print("=> iteration: ", iter+1)

            i = 0

            # Initialize the ants of the ant colony

            for i in range(self.ant_population):

                print("ant population: ", self.ant_population)

                # Initialize the random location
                print("=> ant: ", i+1)
                initial_location = np.random.randint(0, self.environment.get_num_locations())
                print("=> initial_location: ", initial_location)
                
                # Initialize an ant on a random initial location 
                # if iter == 1:
                    # Position the ant in the environment of the ant colony so that it can move around
                ant = Ant(self.alpha, self.beta, initial_location)
                ant.join(self.environment)
                print("debug", self.environment.possible_locations)
                # else:
                #     ant = self.ants[i]
                
                ant.run()

                ant_travel_distance, sum_distance = ant.get_travelled_distance()
                ant_visited_locations = ant.get_visited_location()

                print("=> ant final location: ", ant_visited_locations[-1])

                if sum_distance < shortest_distance:
                    shortest_distance = sum_distance
                    solution = ant_visited_locations

                for i in range(len(ant_visited_locations)-1):
                    location = ant_visited_locations[i]
                    next_location = ant_visited_locations[i+1]
                    self.sum_pheromone[location][next_location] += 1 / ant_travel_distance[i+1]

                # print("=> sum_pheromone: ", self.sum_pheromone)
                
                # Add the ant to the ant colony
                self.ants.append(ant)

                i += 1
                print(i)

            self.environment.update_pheromone_matrix(self.sum_pheromone)

            iter += 1

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(ant_population = 5, iterations = 2, alpha = 1, beta = 2, rho = 0.2)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    