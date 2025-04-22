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
    main_griff_beat = None
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

    #Initialize intersections here


    #Will be filled in when car lengths gotten
    def __init__(self):
        self.main_north_north = numpy.zeros(())
        self.main_north_south = numpy.zeros(())
        self.beat_north = numpy.zeros(())
        self.beat_south = numpy.zeros(())
        self.main_griff_beat = numpy.zeros(())
        self.main_griff_beat_north = numpy.zeros(())
        self.main_griff_beat_south = numpy.zeros(())
        self.griff_east_east = numpy.zeros(())
        self.griff_east_west = numpy.zeros(())
        self.griff_beat_main_east = numpy.zeros(())
        self.griff_beat_main_west = numpy.zeros(())
        self.main_griff_concord_north = numpy.zeros(())
        self.main_griff_concord_south = numpy.zeros(())
        self.concord_east = numpy.zeros(())
        self.concord_west = numpy.zeros(())
        self.main_south_north = numpy.zeros(())
        self.main_south_south = numpy.zeros(())

        #Make the intersections here:
    

    #Segment should:
        #1. Make a car object randomly appear at entrance road arrays
        #2. Make cars move along the roads
        #3. Get rid of end of road cards
        #4. Tell all intersections that a segment has passed
        #5. Click forward time variable
    def time_seg():
        return 0


    