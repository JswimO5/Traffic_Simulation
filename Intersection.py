from car import Car

class intersection:
    exit_locations = None
    stop_signs = None
    last_cycle = None
    def __init__(self, exits, stop_signs):
        """
        Initializes the intersection with a list of roads.
        
        Parameters:
        - exits (list): A nested list of size 4 where exits are put in their repspective directions.
        - stop_signs (list): A list of size 4 where stop signs are put in their respective directions.
        - for both lists directions are: 0 is North, 1 is East, 2 is South, and 3 is West.
        """
        self.exit_locations = exits
        self.stop_signs = stop_signs
        self.last_cycle = [False, False, False, False]

    def _find_direction(self, road):
        """
        Finds the direction of the road in the intersection.
        Parameters:
        - road (int): The road to find the direction for.
        """
        for i in range(4):
            if self.exit_locations[i] != None:
                for j in range(len(self.exit_locations[i])):
                    if self.exit_locations[i][j] == road:
                        break
            if self.exit_locations[i][j] == road:
                        break
        return i

    def _permission_help(self, cars, accepted, roads_leaving):
        """
        Adds cars that can go to the accepted array.
        Parameters:
        - cars: An array of the cars waiting at the intersection of the same priority
        - accepted: array of the cars that have already been accepted
        - roads_leaving: array of booleans representing if the road is fully backed up.
        """
        for car in cars:
            entrance = self._find_direction(car.get_road_from())
            exit = self._find_direction(car.get_road_to())
            if(roads_leaving[exit] != True):
                can_add = True
                for accepted_car in accepted:
                    accepted_to = self._find_direction(accepted_car.get_road_to())
                    accepted_from = self._find_direction(accepted_car.get_road_from())
                    #check is there is any conflict with the car in accepted
                    if accepted_to != exit:
                        #chech strait
                        if abs(entrance-exit) == 2:
                            if accepted_to == ((exit+1) % 4):
                                can_add = False
                                break
                        #check left
                        elif exit == ((entrance+1) % 4):
                            if accepted_from == exit:
                                if accepted_to != entrance:
                                    can_add = False
                                    break
                            elif accepted_to == entrance:
                                can_add = False
                                break
                        #right turn is garenteed based on first if statement
                if can_add == True:
                    accepted.append(car)
        return accepted

    def get_exits(self):
        return self.exit_locations
    
    def give_permission(self, cars, roads_leaving):
        """
        Gives permission to the car to exit the intersection.
        
        Parameters:
        - cars (list): A list of cars that are waiting to cross the intersection.
        - roads_leaving (list): True or false if the road leaving the intersection is backed up.
        - roads_leaving follows the same [N,E,S,W] as the stop_signs list.
        """
        #seperates the cars at the light into different priority groups
        no_stop_signs = []
        right_of_way = []
        last_priority = []
        accepted = []
        for car in cars:
            i = self._find_direction(car.get_road_from())
            if self.stop_signs[i] == True:
                if self.last_cycle[i] == True:
                    last_priority.append(car)
                else:
                    right_of_way.append(car)
            else:
                no_stop_signs.append(car)
        #Goes through the cars by priority group adding cars that don't have conflicts
        #with any previously accepted cars
        if len(no_stop_signs) > 0:
            accepted = self._permission_help(no_stop_signs, accepted, roads_leaving)
        if len(right_of_way) > 0:
            accepted = self._permission_help(right_of_way, accepted, roads_leaving)
        if len(last_priority) > 0:
            accepted = self._permission_help(last_priority, accepted, roads_leaving)
        #logic to record which cars went through the intersection for future priority
        for i in range(4):
            self.last_cycle[i] = False
        for car in accepted:
            came_from = self._find_direction(car.get_road_from())
            self.last_cycle[came_from] = True
        return accepted

            
        
class stop_light(intersection):
    def __init__(self, exits, stop_lights):
        """
        Initializes the intersection with a list of roads.
        Parameters:
        - exits (list): A nested list of size 4 where exits are put in their repspective directions.
        - directions are: 0 is North, 1 is East, 2 is South, and 3 is West.
        - stop_lights (list): list of stop light sequences
        - each sequence is [time,[from,to],[from,to]]
        - times should be accumulative aka [[55...],[71...],[79...]] for concord
        """
        super().__init__(exits, [False]*4)  # Assume no stop signs;
        self.stop_lights = stop_lights 

    def give_permission(self, cars, roads_leaving, time):
        """
        Gives permission to the car to exit the intersection.
        
        Parameters:
        - cars (list): A list of cars that are waiting to cross the intersection.
        - roads_leaving (list): True or false if the road leaving the intersection is backed up.
        - roads_leaving follows the same [N,E,S,W] as the stop_signs list.
        - time: the current time being kept track of by the game board
        """
        right_turns = []
        accepted = []
        #figures out where in the light cycle you are
        time_in_cycle = time % (self.stop_lights[len(self.stop_lights)-1][0])
        for i in range(len(self.stop_lights)):
            if time_in_cycle >= self.stop_lights[i][0]:
                i -= 1
                break
        cycle = self.stop_lights[i]
        #adds cars to respective priority
        for car in cars:
            entrance = self._find_direction(car.get_road_from())
            exit = self._find_direction(car.get_road_to())
            added = False
            #check if the car has a green
            for i in range(1,len(cycle)):
                if cycle[i][0] == entrance and cycle[i][1] == exit:
                    added = True
                    if roads_leaving[exit] != True:
                        accepted.append(car)
                    break
            #checks if the car is turning right and doesn't have green
            if added == False:
                if entrance == ((exit+1) % 4):
                    right_turns.append(car)
        #adds all cars trying to turn right that can
        if len(right_turns) > 0:
            accepted = self._permission_help(right_turns, accepted, roads_leaving)
        return accepted