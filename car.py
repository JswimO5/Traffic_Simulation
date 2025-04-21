import random


class Car:
    #Annual traffic to determine probability of car exits- will be changed in later versions
    GRIFFITH_TO_HIGHWAY = 21000
    BEATY = 6000
    MAIN_STREET_NORTH = 10000
    MAIN_STREET_SOUTH = 13500
    CONCORD = 14000
    total = GRIFFITH_TO_HIGHWAY + BEATY + MAIN_STREET_NORTH + MAIN_STREET_SOUTH + CONCORD

    roadFrom = None
    roadTo = None

    def __init__(self, roadFrom):
        self.roadFrom = roadFrom
        rand = random.randint(1, self.total)
        if rand <= self.GRIFFITH_TO_HIGHWAY:
            self.roadTo = 1
        elif rand <= self.GRIFFITH_TO_HIGHWAY + self.BEATY:
            self.roadTo = 2
        elif rand <= self.GRIFFITH_TO_HIGHWAY + self.BEATY + self.MAIN_STREET_NORTH:
            self.roadTo = 3
        elif rand <= self.GRIFFITH_TO_HIGHWAY + self.BEATY + self.MAIN_STREET_NORTH + self.MAIN_STREET_SOUTH:
            self.roadTo = 4
        else:
            self.roadTo = 5