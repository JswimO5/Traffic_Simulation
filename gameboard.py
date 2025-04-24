import random
import enum
from enum import Enum
import numpy
import car 
from car import Car

class GameBoard:
    


    main_north_north = None
    main_north_south = None
    beat_north = None
    beat_south = None
    main_griff_beat_north = None
    main_griff_beat_south = None
    griff_east_east = None
    griff_east_west = None
    griff_beat_main_east = None
    griff_beat_main_west = None
    main_griff_concord_north = None
    main_griff_concord_south = None
    concord_east = None
    concord_west = None
    main_south_north = None
    main_south_south = None

    exits = []
    entrances = []
    rest = []
    #Initialize intersections here
    norm_roads = []

    #Will be filled in when car lengths gotten
    def __init__(self):
        self.main_north_north = numpy.zeros(0, dtype = Car)
        self.main_north_south = numpy.zeros(0, dtype = Car)
        self.beat_north = numpy.zeros(0, dtype = Car)
        self.beat_south = numpy.zeros(0, dtype = Car)
        self.main_griff_beat_north = numpy.zeros(0, dtype = Car)
        self.main_griff_beat_south = numpy.zeros(0, dtype = Car)
        self.griff_east_east = numpy.zeros(0, dtype = Car)
        self.griff_east_west = numpy.zeros(0, dtype = Car)
        self.griff_beat_main_east = numpy.zeros(0, dtype = Car)
        self.griff_beat_main_west = numpy.zeros(0, dtype = Car)
        self.main_griff_concord_north = numpy.zeros(0, dtype = Car)
        self.main_griff_concord_south = numpy.zeros(0, dtype = Car)
        self.concord_east = numpy.zeros(0, dtype = Car)
        self.concord_west = numpy.zeros(0, dtype = Car)
        self.main_south_north = numpy.zeros(0, dtype = Car)
        self.main_south_south = numpy.zeros(0, dtype = Car)

        self.entrances = [self.main_north_south, self.griff_east_west, self.concord_east, self.main_south_north]
        self.exits = [self.main_north_north, self.griff_east_east, self.concord_west, self.main_south_south]
        #Needs to be made so that they are in a good and fun order
        self.rest = [self.beat_north, self.beat_south, self.main_griff_beat_north, self.main_griff_beat_south,
                 self.griff_beat_main_east, self.griff_beat_main_west, self.main_griff_concord_north, 
                 self.main_griff_concord_south]
        
        #Make the intersections here:
        norm_intersections = [] #Some of these should be duplicated, line up correctly with roads
        entrance_intersections = []
        #Possions
        #Create Poissons for each entrance, include timer, Poission info, and queue of cars
        poosons = []


        #Make real lists here
        for i in range(len(self.rest)-1):
            self.norm_roads.append(self.rest[i], norm_intersections[i])
        for i in range(len(self.entrances)-1):
            self.norm_roads.append(self.entrances[i], entrance_intersections[i], poosons[i])


    def get_rid(exit):
        if exit[len(exit-1)] is not None:
            exit[len(exit-1)] = None
        return exit
    
    def move_cars(road):
        for i in range(len(road)-2, -1, -1):
            if road[i] is not None:
                if road[i+1] is not None:
                    break #Check to see if this breaks correctly
                else:
                    road[i+1] = road[i]
                    road[i] = None
        return road



    #Segment should:
        #1. Make a car object randomly appear at entrance road arrays
        #2. Make cars move along the roads
        #3. Get rid of end of road cards
        #4. Tell all intersections that a segment has passed
        #5. Click forward time variable
    def time_seg(self):
        for road in self.exits:
            self.get_rid(road)
            self.move_cars(road)


        return 0


    