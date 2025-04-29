import random
import enum
from enum import Enum
import numpy
import car 
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
        entrances_roads = [main_north_south, griff_west_west, concord_east, main_south_north]
        self.exits = [main_north_north, griff_west_east, concord_west, main_south_south]
        #Needs to be made so that they are in a good and fun order
        self.rest = [beat_north, beat_south, main_griff_beat_north, main_griff_beat_south,
                 griff_beat_main_east, griff_beat_main_west, main_griff_concord_north, 
                 main_griff_concord_south, main_concord_blake_north, main_concord_blake_south]
        
       
        #make the intersections and gets em together
        beaty_main = Intersection.intersection([[2], None, [3,4], [1]], [False, False, False, True])
        #needs be changed to add sloan
        beaty_griffith = Intersection.stop_light([[2], [3,4], None, [1]], [[48, [1, 3], [3,1]], [8,  [7, 0]], [8, [3, 0]]])
        griffith_main = Intersection.stop_light([[2], None, [3,4], [1]], [[47, [0, 2],[2,0]], [21, [4, 0]], [8, [3, 4]]])
        #need left turning
        concord_main = Intersection.stop_light([[1, 2], [4], [3], None],[[55, [2,0], [0,2]], [16, [1, 0], [1, 2],], [8, [0,1], [0,2]]])
        #This one was kinda confusing, up in the air how we model tbh
        #Also I added some dead time for traffic we arent modeling, fix this if it doesnt work
        main_main = Intersection.stop_light([[1, 2, 4], None, [3], None], [[45, [0,2], [2,0]], [20, [7, 0]]])
        #Add intesection here for potts (currently stopsign)
        #This can be changed to make cars go more efficiently or whatver
        norm_intersections = [beaty_main, beaty_griffith, griffith_main, concord_main, main_main] 


        #Create the queue and poissons for each entrance
        #Create Poissons for each entrance, include timer, Poission info, and queue of cars
        #Need arrival times here
        a1, a2, a3, a4 = 0,0,0,0
        poosons = []
        poosons.append(Que(a1, max_time, 2))
        poosons.append(Que(a2, max_time, 1))
        poosons.append(Que(a3, max_time, 4))
        poosons.append(Que(a4, max_time, 3))
        
        #groups the roads based on intersections 
        bm_int_info = [[main_north_north, None, main_griff_beat_south, beat_south],[main_north_south, None, main_griff_beat_north, beat_north]]
        bg_int_info = [[beat_north, griff_beat_main_east, None, griff_west_west],[beat_south, griff_beat_main_west, None, griff_west_east]]
        gm_int_info = [[main_griff_beat_north, None, main_griff_concord_south, griff_beat_main_west],[main_griff_beat_south, None, main_griff_concord_north, griff_beat_main_east]]
        mc_int_info = [[main_griff_concord_north, concord_east, main_concord_blake_south, None],[main_griff_concord_south, concord_west, main_concord_blake_north, None]]
        mm_int_info = [[main_concord_blake_north, None, main_south_south, None],[main_concord_blake_south, None, main_south_north, None]]
        int_roaders = [bm_int_info, bg_int_info, gm_int_info, mc_int_info, mm_int_info]


        #Makes lists needed for turn incrementing
        for i in range(len(norm_intersections)):
            self.intersections.append([norm_intersections[i], int_roaders[i][0], int_roaders[i][1]]) #This should have a list of an intesection @0 and roads coming out (NESW) @1 roads going in (NESW)
        for i in range(len(self.rest)):
            self.norm_roads.append(self.rest[i])
        for i in range(len(self.entrances)):
            self.norm_roads.append(entrances_roads)
        for i in range(len(self.entrances)):
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
            commute = time - exit_road[last_idx].get_spawn_time()
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
                    break #Check to see if this breaks correctly
                else:
                    road[i+1] = road[i]
                    road[i] = None
        return road

    def _road_packed(self, road):
        if road[0] is None:
            return False
        else:
            return True

    #This can probably be crazy performance improved
    def _move_intersections(self, intersect, accepted, exits, entrances):
        exit_goes = intersect.get_exits()   
        for coar in accepted:
            #removes car from entrance roads
            for entrance in entrances:
                if coar in entrances:
                    entrance[len(entrance-1)] = None
            #Finds the road its going to and checks with intersection to see where it needs to go
            road_to = coar.get_road_to()
            for i in range(len(exit_goes)):
                if road_to in exit_goes[i]:
                    exits[i][0] = coar




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
        for road in self.exits: #This gets rid of cars at exits and moves exit roads forward
            data = self.get_rid(road, time)
            road = data[0]
            if data[1] != 0:
                commutes.append(data[1])
            road = self.move_cars(road)

        #for every intersection; gets list of cars that can move, moves those cars to the next array
        for intersect, exits, enters in range(self.intersections): #This checks what can move and moves them
            north, east, south, west = self.road_packed(exits[0]), self.road_packed(exits[1]), self.road_packed(exits[2]), self.road_packed(exits[3])
            #may need to change cars to get the road currently on?
            coars = []
            for road in enters:
                coars.append(road[len(road)-1])
            if isinstance(intersect, Intersection.stop_light):
                accepted = intersect.give_permission(coars, [north, east, south, west], time)
            else:
                accepted = intersect.give_permission(coars, [north, east, south, west])
            self._move_intersections(intersect, accepted, exits, enters)

        #This moves cars in normal roads and then entrances
        for road in self.norm_roads: 
            road = self.move_cars(road)

        #Make new cars and increment timer on queues for new cars
        for entrance_road, queue in self.entrances: #This makes new cars 
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

 