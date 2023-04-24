
import tsplib95

# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.travelled_distance = 0

    def get_distance(self, location1, location2):
        # location: start (tuple) – n-dimensional coordinate
        tsplib95.distances.euclidean(location1, location2)

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        pass

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):
        prob = []
        self.possible_locations = self.environment.possible_locations
        print("ant possible locations before delete: ", self.possible_locations)
        for i in range(len(self.possible_locations)):
            prob.append(self.environment.pheromone_matrix[self.current_location][i] ** self.alpha * self.environment.distance_matrix[self.current_location][i] ** self.beta)
        max_prob_index = prob.index(max(prob))
        self.current_location = self.possible_locations[max_prob_index]
        del self.possible_locations[max_prob_index]
        print("ant possible locations after delete: ", self.possible_locations)


    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
