import math
from car import Car
import numpy
from collections import deque

class Que:
    """
    Represents a Poisson-based car arrival queue for a given entrance road.

    Simulates random car arrivals over time using an exponential distribution.

    Attributes:
    - queue (deque): A queue of upcoming car arrival times.
    - timer (float): Countdown timer for the next car to be released.
    - road_from (int or entrance Enum): The origin road associated with this queue.
    """

    def __init__(self, arr_p_sec, max_time, road_from):
        """
        Initializes the Poisson arrival queue with randomized arrival times.

        Parameters:
        - arr_p_sec (float): Average arrival rate (cars per second).
        - max_time (float): The total simulation time.
        - road_from (int or entrance): The entrance where cars will spawn from.
        """
        self.queue = deque()
        self.timer = 0
        self.road_from = road_from
        self.car_queue = deque()

        current_time = 0
        neg_sec = -1/arr_p_sec

        while(current_time<max_time):
            r = numpy.random.random() #could be random.random()
            time = round(neg_sec*numpy.log(r))
            current_time += time
            # print(time, road_from)
            self.queue.append(time)

    def car_increment(self, car):
        self.car_queue.append(car)

    def collect(self, time):
        """
        Decrements the timer and returns a new Car when the timer hits 0.

        Parameters:
        - Time: The current time in the simulation.
        
        Returns:
        - Car: A new Car object if it's time for one to arrive.
        - None: If it's not yet time for a new car.
        """
        full = False
        if self.car_queue:
            full = True
        # print ("timer =", self.timer, self.road_from)
        if self.timer <= 0:
            # print("less than 0 ", self.road_from)
            if self.queue:
                self.timer = self.queue.popleft()
                self.timer = self.timer-1
                if not full:
                    return Car(self.road_from, time)
                self.car_queue.append(Car(self.road_from, time))
        else:
            self.timer = self.timer-1
        if full:
            return self.car_queue.popleft()
        return None

