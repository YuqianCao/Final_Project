import math
import numpy as np

CURRENT_YEAR = 2019
class Person:
    def __init__(self, name, year_born):
        self.name = name
        self.year_born = year_born
    def getAge(self):
        return CURRENT_YEAR - self.year_born

    def __str__(self):
        return '{} ({})'.format(self.name, self.getAge())


# class Resident(Person):
#     def __init__(self,name,year_born,knowledge):
#         self.knowledge = knowledge
#         Person.__init__(name,year_born)
#     def study(self):
#         self.knowledge += 1
#
# alice = Resident('Alice Smith',1990)
# print(alice)


class Market:
    def __init__(self, location, level, size):
        self.location = location
        self.level = level
        self.size = size
    def getCost(self):
        return self.level * self.size
    def getDistance(self, home_loc):
        return math.sqrt(np.square(self.location[0] - home_loc[0]) + np.square(self.location[1] - home_loc[1]))




market1 = Market((3,4),1,5)
store = (1,1)
print(market1.getDistance(store))
