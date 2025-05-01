import random
import enum
from enum import Enum
#TESTING NEEDED 

#Further improvements: 
#Car size, car speed max, current car speed
#roadto is a factor of roadfrom - can do worst case scenarios, or just make it more likely to go farther
#Car behavior- whether they prefer going somewhere with traffic or somewhere slower but without

#If needed in implimentation:
#randomizes roadfrom 

#Ensure that ints in main class align with entrance enum vals, or is enum
class entrance(Enum):
    """
    Enum class representing possible exit roads a car may take.
    Helps improve readability and avoid bugs related to string usage.
    """
    griffith = 1
    main_north = 2
    main_south = 3
    concord = 4


class Car:
    """
    Class representing a car in the traffic simulation.

    Attributes:
    - roadFrom (entrance): The road the car starts from.
    - roadTo (entrance): The road the car is heading to.
    """
    #Annual traffic to determine probability of car exits- will be changed in later versions
    #Change could be factoring that many people want to leave at the same time (rush hour)
    GRIFFITH_TO_HIGHWAY = 17000
    MAIN_STREET_NORTH = 10000
    MAIN_STREET_SOUTH = 13500
    CONCORD = 14000
    total = GRIFFITH_TO_HIGHWAY + MAIN_STREET_NORTH + MAIN_STREET_SOUTH + CONCORD

    #These are enums, can explain later if you want. Could be super helpful in other situations
    #They are mostly used to make the code readable and avoid stupid bugs 

    def __init__(self, roadFrom, time):
        """
        Initializes a new car object with a random destination based on traffic distribution.

        Parameters:
        - roadFrom (entrance): The origin road where the car starts its journey.
        - time: The current time in the simulation when the car is being spawned.
        """
        self.roadTo = None
        self.roadFrom = entrance(roadFrom)
        self.spawn = time
        
        while self.roadTo is None or self.roadTo == self.roadFrom:
            
            rand = random.randint(1, self.total)
            if rand <= self.GRIFFITH_TO_HIGHWAY:
                self.roadTo = entrance.griffith
            elif rand <= self.GRIFFITH_TO_HIGHWAY + self.MAIN_STREET_NORTH:
                self.roadTo = entrance.main_north
            elif rand <= self.GRIFFITH_TO_HIGHWAY + self.MAIN_STREET_NORTH + self.MAIN_STREET_SOUTH:
                self.roadTo = entrance.main_south
            else:
                self.roadTo = entrance.concord

    def get_road_from(self):
        """
        Retrieves the origin road of the car.

        Returns:
        - entrance: The road the car started from.
        """
        return self.roadFrom.value
    
    def get_road_to(self):
        """
        Retrieves the destination road of the car.

        Returns:
        - entrance: The road the car is heading to.
        """
        return self.roadTo.value
    
    def get_spawn_time(self):
        """
        Retrieves the spawn time of the car.

        Returns:
        - spawn: The time the car spawned at.
        """
        return self.spawn