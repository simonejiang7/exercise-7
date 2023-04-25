
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
        self.visited_locations = [initial_location]
        self.travelled_distance = [0]
        self.first = True

    def get_distance(self, location1, location2):
        coord1 = self.environment.get_location_coords(location1)
        coord2 = self.environment.get_location_coords(location2)
        return tsplib95.distances.euclidean(coord1, coord2)

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        
        if self.first:
            self.possible_locations = self.environment.get_possible_locations().copy()
        self.first = False

        del self.possible_locations[self.possible_locations.index(self.current_location)]

        if self.possible_locations:
            self.select_path()
            self.run()

        else:
            
            assert len(self.visited_locations) == self.environment.get_num_locations()
            assert len(self.travelled_distance) == self.environment.get_num_locations()
            print("=> finished iteration")

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):

        prob_list = []

        self.pheromone_matrix = self.environment.get_pheromone_matrix()

        for possible_location in self.possible_locations:
            current_to_j = (self.pheromone_matrix[self.current_location][possible_location] ** self.alpha) * (self.environment.distance_matrix[self.current_location][possible_location] ** self.beta)
            sum_current_to_l = sum([(self.pheromone_matrix[self.current_location][l] ** self.alpha) * (self.environment.distance_matrix[self.current_location][l] ** self.beta) for l in self.possible_locations])
            prob = current_to_j / sum_current_to_l
            prob_list.append(prob)

        assert len(prob_list) == len(self.possible_locations)
        max_prob_index = prob_list.index(max(prob_list))
        future_location = self.possible_locations[max_prob_index]

        self.travelled_distance.append(self.get_distance(self.current_location, future_location))
        self.current_location = future_location
        self.visited_locations.append(self.current_location)

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    def get_visited_locations(self):
        return self.visited_locations
    
    def get_travelled_distance(self):
        return self.travelled_distance, sum(self.travelled_distance)
