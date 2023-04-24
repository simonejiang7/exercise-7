
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
        self.travelled_distance = 0

    def get_distance(self, location1, location2):
        coord1 = self.environment.get_location_coords(location1+1)
        coord2 = self.environment.get_location_coords(location2+1)
        return tsplib95.distances.euclidean(coord1, coord2)

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        self.possible_locations = self.environment.get_possible_locations()
        del self.possible_locations[self.possible_locations.index(self.current_location)]

        if self.possible_locations:
            self.select_path()
            self.run()
        else:
            print("=> ant visited locations: ", self.visited_locations)
            assert len(self.visited_locations) == self.environment.get_num_locations()
            print("=> ant travelled distance: ", self.travelled_distance)
            print("=> ant current location: ", self.current_location)
            print("=> finished iteration")
    

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):

        prob_list = []

        # self.possible_locations = self.environment.get_possible_locations(self.current_location)
        # del self.possible_locations[self.possible_locations.index(self.current_location)]
        print("=> current location is: ", self.current_location)
        print("=> ant possible locations before moving: ", self.possible_locations)

        self.pheromone_matrix = self.environment.get_pheromone_matrix()

        for possible_location in self.possible_locations:
            current_to_j = self.pheromone_matrix[self.current_location][possible_location] ** self.alpha + self.environment.distance_matrix[self.current_location][possible_location] ** self.beta
            # print("FOR DEBUGGING: all possible locations list", [self.pheromone_matrix[self.current_location][l] ** self.alpha + self.environment.distance_matrix[self.current_location][l] ** self.beta for l in self.possible_locations])
            sum_current_to_l = sum([self.pheromone_matrix[self.current_location][l] ** self.alpha + self.environment.distance_matrix[self.current_location][l] ** self.beta for l in self.possible_locations])
            prob = current_to_j / sum_current_to_l
            # print("prob: ", prob)
            prob_list.append(prob)

        max_prob_index = prob_list.index(max(prob_list))
        # print("max_prob_index: ", max_prob_index)
        # print("FOR DEBUGGING: prob list ", prob_list)
        
        # Update the travelled distance of the ant

        future_location = self.possible_locations[max_prob_index]

        print("=> current location is: ", self.current_location)
        print("=> future location is: ", future_location)
              
        self.travelled_distance += self.get_distance(self.current_location, self.possible_locations[max_prob_index])
        print("=> ant travelled distance: ", self.get_distance(self.current_location, self.possible_locations[max_prob_index]))
        print("=> ant travelled distance: ", self.environment.distance_matrix[self.current_location][self.possible_locations[max_prob_index]])
        assert self.get_distance(self.current_location, self.possible_locations[max_prob_index]) == self.environment.distance_matrix[self.current_location][self.possible_locations[max_prob_index]]
        self.current_location = self.possible_locations[max_prob_index]

        self.visited_locations.append(self.current_location)
        # del self.possible_locations[max_prob_index]
        # print("=> ant possible locations after moving: ", self.possible_locations)

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    def get_visited_locations(self):
        return self.visited_locations
