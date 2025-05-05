import random
from enum import Enum
import numpy
from car import Car
from poisson import Que
import Intersection

class GameBoard:
    """
    Represents the main simulation board containing all roads, entrances, exits, 
    and the core logic for simulating traffic over time.

    Attributes:
    - Road segments (numpy arrays): Each road holds a series of car objects or empty slots.
    - entrances (list): Entrances to the road network where cars can spawn.
    - exits (list): Exits from the road network where cars leave.
    - rest (list): Internal road segments used for movement between intersections.
    - norm_roads (list): Combination of all roads, linked with intersections and Poisson queues.
    """


    #Initialize global arrays
    exits = []
    entrances = []
    rest = []
    intersections = []
    norm_roads = []


    #Will be filled in when car lengths gotten
    def __init__(self, max_time):
        """
        Initializes all road arrays, entrance/exit lists, Poisson queues, 
        and links roads to intersections.

        Parameters:
        - max_time (int): The total time for which the simulation runs.
        """

        #List all roads with num of cars that that they can have
        main_north_north = [None] *30
        main_north_south = [None] *30
        beat_north = [None] *264
        beat_south = [None] *264
        main_griff_beat_north = [None] *178
        main_griff_beat_south = [None] *178
        griff_west_east = [None] *147
        griff_west_west = [None] *147
        griff_beat_main_east = [None] *88
        griff_beat_main_west = [None] *88
        main_griff_concord_north = [None] *51
        main_griff_concord_south = [None] *51
        concord_east = [None] *50 #This is an arbitrary number, if there is a better idea, I would love to hear it
        concord_west = [None] *50
        main_concord_blake_north= [None] *25
        main_concord_blake_south= [None] *25
        main_south_north = [None] *293 #Will need to be changed to add potts intersection
        main_south_south = [None] *293

        #Groups the roads based on exit, entrance, and rest
        entrances_roads = [main_north_south, griff_west_east, concord_west, main_south_north]
        self.exits = [main_north_north, griff_west_west, concord_east, main_south_south]
        #Needs to be made so that they are in a good and fun order
        self.rest = [beat_north, beat_south, main_griff_beat_north, main_griff_beat_south,
                 griff_beat_main_east, griff_beat_main_west, main_griff_concord_north, 
                 main_griff_concord_south, main_concord_blake_north, main_concord_blake_south]
        
       
        #make the intersections and gets em together
        beaty_main = Intersection.intersection([[2], None, [3,4], [1]], [False, False, False, True])
        #needs be changed to add sloan
        beaty_griffith = Intersection.stop_light([[2], [3,4], None, [1]], [[96, [1, 3], [3,1]], [112,  [0, 3]], [128, [3, 0]]])
        griffith_main = Intersection.stop_light([[2], None, [3,4], [1]], [[94, [0, 2],[2,0], [0, 3]], [134, [3, 0], [3,2]], [150, [2, 3]]])
        #need left turning
        concord_main = Intersection.stop_light([[1, 2], [4], [3], None],[[110, [2,0], [0,2], [2, 1]], [142, [1, 0], [1, 2]], [181, [0,1], [0,2]], [190, [7,0]]])
        #This one was kinda confusing, up in the air how we model tbh
        #Also I added some dead time for traffic we arent modeling, fix this if it doesnt work
        main_main = Intersection.stop_light([[1, 2, 4], None, [3], None], [[120, [0,2], [2,0]]])
        #Add intesection here for potts (currently stopsign)
        #This can be changed to make cars go more efficiently or whatver
        norm_intersections = [beaty_main, beaty_griffith, griffith_main, concord_main, main_main] 


        #Create the queue and poissons for each entrance
        #Create Poissons for each entrance, include timer, Poission info, and queue of cars
        #Need arrival times here
        a1, a2, a3, a4 = .03561,.04928,.0925,.0825 
        poosons = []
        poosons.append(Que(a1, max_time, 2))
        poosons.append(Que(a2, max_time, 1))
        poosons.append(Que(a3, max_time, 4))
        poosons.append(Que(a4, max_time, 3))
        
        #groups the roads based on intersections #third index is left turn lanes at {N,E,S,W}
        bm_int_info = [[main_north_north, None, main_griff_beat_south, beat_south],[main_north_south, None, main_griff_beat_north, beat_north], [False, False, False, False]]
        bg_int_info = [[beat_north, griff_beat_main_east, None, griff_west_west],[beat_south, griff_beat_main_west, None, griff_west_east], [False, True, False, True]]
        gm_int_info = [[main_griff_beat_north, None, main_griff_concord_south, griff_beat_main_west],[main_griff_beat_south, None, main_griff_concord_north, griff_beat_main_east], [False, True, True, False]]
        mc_int_info = [[main_griff_concord_north, concord_east, main_concord_blake_south, None],[main_griff_concord_south, concord_west, main_concord_blake_north, None], [False, True, False, True]]
        mm_int_info = [[main_concord_blake_north, None, main_south_south, None],[main_concord_blake_south, None, main_south_north, None], [False, False, False, False]]
        int_roaders = [bm_int_info, bg_int_info, gm_int_info, mc_int_info, mm_int_info]


        #Makes lists needed for turn incrementing
        for i in range(len(norm_intersections)):
            self.intersections.append([norm_intersections[i], int_roaders[i][0], int_roaders[i][1], int_roaders[i][2]]) #This should have a list of an intesection @0 and roads coming out (NESW) @1 roads going in (NESW)
        for i in range(len(self.rest)):
            self.norm_roads.append(self.rest[i])
        for i in range(len(entrances_roads)):
            self.norm_roads.append(entrances_roads[i])
        for i in range(len(entrances_roads)):
            self.entrances.append([entrances_roads[i], poosons[i]])
        
       


    def get_rid(self, exit_road, time):
        """
        Removes a car from the end of an exit road, simulating that it has left the system.

        Parameters:
        - exit (numpy array): The road from which to remove the car.

        Returns:
        - numpy array: The updated road after removal.
        - the commute time of the car that left. If no car leaves, commute equals zero.
        """
        last_idx = len(exit_road) - 1
        commute = 0
        if exit_road[last_idx] is not None:
            #calulate commute
            #print(exit_road)
            commute = exit_road[last_idx]
            exit_road[last_idx] = None
        return [exit_road, commute]
    
    def move_cars(self, road):
        """
        Moves cars forward along a given road segment if the next position is empty.

        Parameters:
        - road (numpy array): The road segment where car movement is simulated.

        Returns:
        - numpy array: The updated road with moved cars.
        """

        

        for i in range(len(road)-2, -1, -1):
            if road[i] is not None:
                if road[i+1] is not None:
                    continue
                else:
                    road[i+1] = road[i]
                    road[i] = None
        return road

    def _road_packed(self, road):

        try:
            return road[0] is not None
        except (TypeError, IndexError):
            return False

    #This can probably be crazy performance improved
    def _move_intersections(self, intersect, accepted, exits, entrances):
        # if accepted[0].get_road_from() != 2 and accepted[0].get_road_from() != 3:
        #     print(accepted[0].get_road_from())
        exit_goes = intersect.get_exits() 
        for coar in accepted:
            #removes car from entrance roads
            for entrance in entrances:
                if entrance is not None and coar in entrance:
                    for i in range(len(entrance)):
                        if entrance[i] is not None and entrance[i]== coar:
                            entrance[i] = None
                            break
            #Finds the road its going to and checks with intersection to see where it needs to go
            road_to = coar.get_road_to()
            for i in range(len(exit_goes)):
                if exit_goes[i] is not None:
                    if road_to in exit_goes[i]:
                        exits[i][0] = coar

    #Ripped this from chatgpt
    def _get_turn_direction(self, entrance_idx, exit_idx):
        """
        Determines if a car is turning left, right, or going straight based on entrance and exit indices.
        
        Parameters:
        - entrance_idx: Index representing entrance direction (0=N, 1=E, 2=S, 3=W)
        - exit_idx: Index representing exit direction (0=N, 1=E, 2=S, 3=W)
        
        Returns:
        - int: right lane returns with a 1, left with a 2
        """
        if entrance_idx < 0 or exit_idx < 0:
            return None
            
        # Calculate turn direction using modulo arithmetic
        # Subtract 1 for left turn, add 1 for right turn (mod 4)
        diff = (exit_idx - entrance_idx) % 4
        
        if diff == 0:
            return 1
        elif diff == 1:
            return 1
        elif diff == 3:
            return 2


    def _le_turners(self, intersection, j, car):
        exit_goes = intersection[0].get_exits()
        roader = car.get_road_to()
        index = -1
        for i in range(len(exit_goes)):
            if roader in exit_goes[i]:
                index = i
                break    
        for i in range(1, 5):
            try:
                roader_cool = intersection[2][j][-(i+1)].get_road_to()
            except(AttributeError):
                continue
            for k in range(len(exit_goes)):
                if roader_cool in exit_goes[k]:
                    index2 = k
                    break    
            if self._get_turn_direction(j, index) != self._get_turn_direction(j, index2):
                return intersection[2][j][-(i+1)]
        return None



    def time_seg(self, time):
        """
        Advances the simulation by one time segment.

        Operations include:
        1. Removing cars from exits
        2. Moving cars within roads
        3. Managing intersections (placeholder)
        4. Introducing new cars from entrance queues

        Returns:
        - an array of the commute times for the cars exiting on that cycle
        """
        commutes = []
        for i in range(len(self.exits)): #This gets rid of cars at exits and moves exit roads forward
            data = self.get_rid(self.exits[i], time)
            self.exits[i] = data[0]
            if data[1] != 0:
                commutes.append(data[1])
            self.exits[i] = self.move_cars(self.exits[i])


        #for every intersection; gets list of cars that can move, moves those cars to the next array
        for i in range(len(self.intersections)): #This checks what can move and moves them
            north, east, south, west = self._road_packed(self.intersections[i][1][0]), self._road_packed(self.intersections[i][1][1]), self._road_packed(self.intersections[i][1][2]), self._road_packed(self.intersections[i][1][3])
            # if i == 3:
            #     print(east)
            #may need to change cars to get the road currently on?
            coars = []
            for j in range(len(self.intersections[i][2])):
                try:
                    if self.intersections[i][2][j] is not None and len(self.intersections[i][2][j]) > 0:
                        fin = self.intersections[i][2][j][-1]
                        if fin is not None:  
                            coars.append(fin)
                            if self.intersections[i][3][j] and self.intersections[i][2][j][-2] is not None:
                                more_car = self._le_turners(self.intersections[i], j, fin)
                                if more_car is not None:
                                    coars.append(more_car)
                except (TypeError, IndexError):
                    pass
            if isinstance(self.intersections[i][0], Intersection.stop_light):
                accepted = self.intersections[i][0].give_permission(coars, [north, east, south, west], time)
            else:
                accepted = self.intersections[i][0].give_permission(coars, [north, east, south, west])
            if len(accepted) > 0:
                self._move_intersections(self.intersections[i][0], accepted, self.intersections[i][1], self.intersections[i][2])

        #This moves cars in normal roads and then entrances
        for i in range(len(self.norm_roads)): 
            self.norm_roads[i] = self.move_cars(self.norm_roads[i])

        #Make new cars and increment timer on queues for new cars
        for entrance_road, queue in self.entrances: #This makes new cars 
            #print("Anything")
            coar = queue.collect(time)
            if(coar != None):
                if self._road_packed(entrance_road):
                    queue.car_increment(coar)
                entrance_road[0] = coar
        return commutes

            
    def print_all(self):
        print("Each array shows where cars are in that array. Consult constructor to find order of roads")
        print("Exits: ")
        for road in self.exits:
            cars_at = []
            for i in range(len(road)):
                if road[i] is not None:
                    cars_at.append(i)
            print(cars_at)
        print("Entrances: ")
        for road, queue in self.entrances:
            cars_at = []
            for i in range(len(road)):
                if road[i] is not None:
                    cars_at.append(i)
            print(cars_at)
        print("Rest of roads: ")
        for road in self.rest:
            cars_at = []
            for i in range(len(road)):
                if road[i] is not None:
                    cars_at.append(i)
            print(cars_at)

 