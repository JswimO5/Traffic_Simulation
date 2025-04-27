import math
from car import Car
import numpy
from collections import deque

class que:

    queue = deque()
    timer = 0
    road_from = 0

    def __init__(self, arr_p_sec, max_time, road_from):
        self.road_from = road_from
        timer = 0
        neg_sec = -1/arr_p_sec
        while(timer<max_time):
            r = numpy.random()
            time = neg_sec*numpy.log(r)
            timer += time
            self.queue.put(time)

    def collect(self):
        if self.timer == 0:
            timer = self.queue.pop(0)
            timer = timer-1
            return Car(self.road_from)
        else:
            timer = timer-1
        return None

