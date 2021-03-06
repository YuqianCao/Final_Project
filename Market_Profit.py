import math
import numpy as np
import matplotlib.pyplot as plt
import threading


price_level = {'level1': 5,
               'level2': 15,
               'level3': 30,
               'level4': 50,
               'level5': 80}

income_level = {"low": 300,
                "median": 1000,
                "high": 2000}

level_style = {'level1': '.',
               'level2': 'o',
               'level3': '^',
               'level4': '*',
               'level5': '|'}

level_color = {'level1': 'red',
               'level2': 'blue',
               'level3': 'green',
               'level4': 'grey',
               'level5': 'orange'}



class Market:
    def __init__(self, location, level:str, size:int):
        '''
        Each Market object represents the basic info and the profit of the corresponding market.
        :param location: the location coordinate of a certain market
        :param level: the price level of the Market. From level1 to level5. The higher the level, the more expensive it is.
        :param size: the maximum capacity of the market
        '''
        self.location = location
        self.buy_price = price_level[level]
        self.sell_price = self.buy_price * 2
        self.size = size
        self.level = level
    def getCost(self):
        '''
        :return: the total cost for running the store, including stock with goods and hiring fee.
        '''
        return self.buy_price * self.size * 1.2
    def getProfit(self, cust_num):
        '''
        :param cust_num: the number of the customer that will purchase in this market
        :return: the total profit for running this store (calculate by income - cost)
        '''
        return self.sell_price * min(cust_num,self.size) - self.getCost()


class Resident:
    def __init__(self, level:str, home_loc):
        '''
        :param level: the income level for the resident, could be low, median or high.
        :param home_loc: the coordinate of the resident's home
        '''
        self.income = income_level[level]
        self.home_loc = home_loc
    def getBudget(self):
        '''
        :return: the maximum shopping budget that the resident can afford.
        '''
        return self.income/10
    def getDistance(self, location):
        '''
        :param location: the location coordinate of a certain market
        :return: the distance between the resident's home to the market
        '''
        return math.sqrt(np.square(self.home_loc[0] - location[0]) + np.square(self.home_loc[1] - location[1]))
    def purchase(self, price, location, size):
        '''
        :param price: the average selling price of a certain market
        :param location: the location coordinate of a certain market
        :param size: the maximum capacity of a certain market
        :return: whether the resident would purchase in the certain market. "True" represents the resident will purchase goods, vice versa.
        '''
        if self.getBudget() >= price and self.getDistance(location) <= math.sqrt(size):
            return True
        else:
            return False

class Company:
    def __init__(self,budget:int):
        '''
        :param budget: the total budget of this company
        '''
        self.budget = budget
    def getMaxamount(self,Market):
        '''
        Given a certain Market object, we will calculate according to the company's budget, how many markets with the same size and level can be started at most.
        :param Market: a certain market object
        :return: the upper limitation of the number of the markets that could be started by the company.
        '''
        return self.budget/Market.getCost()


def getMap(row:int, col:int, rich_area:list, poor_area:list):
    '''
    This function allow users to create a city map by input the city size and the location of wealthy area and poor area.
    :param row: The rows of the entire city
    :param col: The columns of the entire city
    :param rich_area: a list, contains the start point and end point of wealthy area.
    :param poor_area: a list, contains the start point and end point of poor area.
    :return: a map of a city
    >>> getMap((1, 1, [[0, 0], [0, 0]], [[0, 0], [0, 0]]))
    [[0]]
    >>> getMap(getMap(4, 5, [[1, 2], [3, 4]], [[7, 8], [8, 8]]))
    [[1 1 1 1 1]
     [1 1 2 2 2]
     [1 1 2 2 2]
     [1 1 2 2 2]]
    >>> test_map = getMap(getMap(70, 80, [[1, 2], [3, 4]], [[7, 8], [8, 8]]))
    >>> test_map.size
    5600
    '''
    map = np.ones([row, col], dtype=int)
    rich_start = rich_area[0]
    rich_end = rich_area[1]
    poor_start = poor_area[0]
    poor_end = poor_area[1]
    map[rich_start[0]:rich_end[0]+1,rich_start[1]:rich_end[1]+1] = 2
    map[poor_start[0]:poor_end[0]+1,poor_start[1]:poor_end[1]+1] = 0
    return map


def getResidents(map):
    '''
    Assume that we already have a map of a city, this function will generate a list of Resident according to your map.
    :param map: The map of the city
    :return: a list of Resident objects
    >>> test_map =  getMap(10, 10, [[0, 0], [0, 0]], [[0, 0], [0, 0]])
    >>> test_Resident = getResidents(test_map)
    >>> len(test_Resident) == test_map.size
    True
    '''
    resident_list = []
    map_row = map.shape[0]
    map_col = map.shape[1]
    for i in range(0,map_row):
        row_list = []
        for j in range(0,map_col):
            if map[i][j] == 2:
                resident = Resident('high',(i,j))
                row_list.append(resident)
            elif map[i][j] == 1:
                resident = Resident('median',(i,j))
                row_list.append(resident)
            else:
                resident = Resident('low', (i, j))
                row_list.append(resident)
        resident_list.append(row_list)
    return resident_list


def randomStoreLoc(map,amount:int,uniform:bool):
    '''
    Randomly generate the location of the markets on the map.
    :param map: city map
    :param amount: the number of markets to be generated
    :param uniform: bool type, true means make the stores uniform distributed among the city
    :return: a list of market location
    >>> test_map =  getMap(10, 10, [[0, 0], [0, 0]], [[0, 0], [0, 0]])
    >>> test_map.size
    100
    >>> test_Resident = getResidents(test_map)
    >>> test_market = Market((0, 0), "level2", 40)
    >>> amount = 40
    >>> store_list = randomStoreLoc(test_map,amount,True)
    >>> len(store_list)
    40
    '''
    map_row = map.shape[0]
    map_col = map.shape[1]
    map_size = map.size
    store_loc_list = []
    if uniform == False:
        for store in range(amount):
            store_row = np.random.randint(low=0, high=map_row, size=1, dtype=int)
            store_col = np.random.randint(low=0, high=map_col, size=1, dtype=int)
            store_loc = [store_row[0],store_col[0]]
            store_loc_list.append(store_loc)
    else:
        interval = int(map_size / (amount-1))
        loc_num = np.arange(0,map_size,interval)
        for num in loc_num:
            if (num+1)%map_row == 0:
                store_row = int(((num+1)/map_row)-1)
                store_col = map_col-1
                store_loc = [store_row, store_col]
                store_loc_list.append(store_loc)
            else:
                store_row = int((num+1)/map_row)
                store_col = num - store_row * map_col
                store_loc = [store_row, store_col]
                store_loc_list.append(store_loc)

    return store_loc_list

def getMarkets(store_loc_list,level,size):
    '''
    Given a list of store location, this function will automatically generate corresponding Market class
    :param store_loc_list: the list of store location
    :param level: the level of stores to be generated
    :param size: the size of markets
    :return: a list of Market objects
    >>> test_map =  getMap(10, 10, [[0, 0], [0, 0]], [[0, 0], [0, 0]])
    >>> test_map.size
    100
    >>> test_Resident = getResidents(test_map)
    >>> test_market = Market((0, 0), "level2", 40)
    >>> amount = 50
    >>> store_list = randomStoreLoc(test_map,amount,True)
    >>> len(getMarkets(store_list), "level2", 40)
    50
    '''
    market_list = []
    for loc in store_loc_list:
        new_market = Market(loc,level,size)
        market_list.append(new_market)
    return market_list


def getCustAmount(Market:object,resident_list:list):
    """
    For specific market, given a list of Resident objects, this function will calculate the amount of residents that will purchase in this market.
    :param Market: the target market object
    :param resident_list: the list of Resident object
    :return: the number of customers
    >>> test_map = getMap(10, 10, [[0, 0], [0, 0]], [[0, 0], [0, 0]])
    >>> test_Resident = getResidents(test_map)
    >>> test_market = Market((0, 0), "level2", 40)
    >>> getCustAmount(test_market, test_resident) <= test_map.size
    True
    """
    cust_num = 0
    for row in resident_list:
        for resident in row:
            if resident.purchase(Market.sell_price, Market.location, Market.size) == True:
                cust_num += 1
    return cust_num

def getTotalProfit(market_list, resident_list):
    '''
    Given a list of Market object and a list of Resident object, this function will calculate the total profit of all the markets
    :param market_list: a list of Market object
    :param resident_list: a list of Resident object
    :return: the amount of total profit
    '''
    total_profit = 0
    for market in market_list:
        cust_num = getCustAmount(market,resident_list)
        profit = market.getProfit(cust_num)
        total_profit += profit
    return total_profit

def sizeProfitPlot(map,resident,company,possible_size,city_type):
    '''
    This function will generate a line plot which demonstrate the relationship between the size of supermarket and the total profit.
    :param map: The city map
    :param resident: a list of resident object
    :param company: a company object
    :param possible_size: a list of possible size
    :param city_type: the type of the city, used to generated the name of the x-axis of the plot.
    :return:
    '''
    plt.cla
    for level in price_level:
        profit = []
        for size in possible_size:
            test_market = Market((0, 0), level, size)
            random_loc = randomStoreLoc(map, company.getMaxamount(test_market), True)
            rand_markets = getMarkets(random_loc, level, size)
            profit.append(getTotalProfit(rand_markets, resident))
        plt.title('Relationship Between Size and Profit')
        plt.plot(possible_size,profit,marker=level_style[level],color=level_color[level],label=level)
    plt.xlabel('Size of market(persons)')
    plt.ylabel('Profit($)')
    plt.legend()
    plt.savefig(city_type)
    plt.close('all')

def levelProfitPlot(map,resident,company,size):
    '''
    Given a map and a list of residents, this function will generate a plot that demonstrated the relationship between the distribution style, market level and the total profit.
    :param map: The map of the city
    :param resident: a list of Resident object
    :param company: a company object
    :param size: the size of the market
    :return:
    '''
    plt.cla
    level_list = price_level.keys()
    profit_uni = []
    for level in level_list:
        test_market = Market((0, 0), level, size)
        loc = randomStoreLoc(map, int(company.getMaxamount(test_market)), True)
        markets_list = getMarkets(loc, level, size)
        profit_uni.append(getTotalProfit(markets_list, resident))
    plt.title('The Influence of Market Distribution')
    plt.plot(level_list, profit_uni, "g+-", label="Uniform Distribution")
    profit_rand = []

    def random_test(level, size, times):
        pro_sum = 0
        for count in range(times):
            test_market = Market((0, 0), level, size)
            loc = randomStoreLoc(map, int(company.getMaxamount(test_market)), False)
            markets_list = getMarkets(loc, level, size)
            pro_sum += getTotalProfit(markets_list, resident)
        avg_pro = pro_sum/times
        return avg_pro

    for level in level_list:
        profit_rand.append(random_test(level,size,100))
    plt.plot(level_list, profit_rand, 'r^-', label="Random Distribution")
    plt.xlabel('Level Of Market')
    plt.ylabel('Total Profit($)')
    plt.legend()
    plt.savefig('MarkerDistributionVsProfit')
    plt.close('all')


def main():

    companyA = Company(15000)
    city_row = 100
    city_col = 100
    cityMap = getMap(city_row, city_col, [[0, 0], [40, 40]], [[60, 60], [99, 99]])
    # Generate a city (average income) map with 100 rows and 100 columns, rich area is from (0,0) to (40,40), low-income area is from (60,60) to (99,99)
    rich_cityMap = getMap(city_row, city_col, [[0, 0], [70, 70]], [[90, 90], [99, 99]])
    poor_cityMap = getMap(city_row, city_col, [[0, 0], [10, 10]], [[30, 30], [99, 99]])
    cityResident = getResidents(cityMap)
    rich_cityResident = getResidents(rich_cityMap)
    poor_cityResident = getResidents(poor_cityMap)


    # simulation for hypothesis one:
    # The best size and level of supermarkets to be started is related to the population and income level
    possible_size = range(10,80,10)
    sizeProfitPlot(cityMap,cityResident,companyA,possible_size,"averageCity")
    sizeProfitPlot(rich_cityMap, rich_cityResident, companyA, possible_size, "richCity")
    sizeProfitPlot(poor_cityMap, poor_cityResident, companyA, possible_size, "poorCity")


    # simulation for hypothesis two:
    # simulation for random distribution and even distribution
    levelProfitPlot(cityMap,cityResident,companyA,40)


if __name__ == '__main__':
    main()


