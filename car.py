import random


class Car:
    #Annual traffic to determine probability of car exits- will be changed in later versions
    GRIFFITH_TO_HIGHWAY = 21000
    BEATY = 6000
    MAIN_STREET_NORTH = 10000
    MAIN_STREET_SOUTH = 13500
    CONCORD = 14000


    roadFrom = None
    roadTo = None

    def __init__(self, roadFrom):
        self.roadFrom = roadFrom
