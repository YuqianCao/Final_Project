import math
import numpy as np
import matplotlib.pyplot as plt


price_level = {'level1': 5,
               'level2': 15,
               'level3': 30,
               'level4': 50,
               'level5': 100}

income_level = {"low": 300,
                "median": 1000,
                "high": 2000}

level_style = {'level1': '.',
               'level2': 'o',
               'level3': '^',
               'level4': '*',
               'level5': '_'}

level_color = {'level1': 'red',
               'level2': 'blue',
               'level3': 'green',
               'level4': 'grey',
               'level5': 'orange'}

class Market:
    def __init__(self, location, level:str, size:int):
        self.location = location
        self.buy_price = price_level[level]
        self.sell_price = self.buy_price * 2
        self.size = size
        self.level = level
    def getCost(self):
        return self.buy_price * self.size * 1.2
    def getProfit(self, cust_num):
        return self.sell_price * min(cust_num,self.size) - self.getCost()


class Resident:
    def __init__(self, level:str, home_loc):
        self.income = income_level[level]
        self.home_loc = home_loc
    def getBudget(self):
        return self.income/10
    def getDistance(self, location):
        return math.sqrt(np.square(self.home_loc[0] - location[0]) + np.square(self.home_loc[1] - location[1]))
    def purchase(self, price, location, size):
        if self.getBudget() >= price and self.getDistance(location) <= math.sqrt(size):
            return True
        else:
            return False

class Company:
    def __init__(self,budget:int):
        self.budget = budget
    def getMaxamount(self,Market):
        return self.budget/Market.getCost()


def getMap(row:int, col:int, rich_area:list, poor_area:list):
    map = np.ones([row, col], dtype=int)
    rich_start = rich_area[0]
    rich_end = rich_area[1]
    poor_start = poor_area[0]
    poor_end = poor_area[1]
    map[rich_start[0]:rich_end[0]+1,rich_start[1]:rich_end[1]+1] = 2
    map[poor_start[0]:poor_end[0]+1,poor_start[1]:poor_end[1]+1] = 0
    return map


def getResidents(map):
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
    market_list = []
    for loc in store_loc_list:
        new_market = Market(loc,level,size)
        market_list.append(new_market)
    return market_list


def getCustAmount(Market:object,resident_list:list):
    cust_num = 0
    for row in resident_list:
        for resident in row:
            if resident.purchase(Market.sell_price, Market.location, Market.size) == True:
                cust_num += 1
    return cust_num

def getTotalProfit(market_list, resident_list):
    total_profit = 0
    for market in market_list:
        cust_num = getCustAmount(market,resident_list)
        profit = market.getProfit(cust_num)
        total_profit += profit
    return total_profit

def sizeProfitPlot(map,resident,company,possible_size,city_type):
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
    plt.xlabel('Size of market')
    plt.ylabel('Profit')
    plt.legend()
    plt.savefig(city_type)
    plt.close('all')



def main():

    companyA = Company(10000)
    city_row = 100
    city_col = 100
    cityMap = getMap(city_row, city_col, [[0, 0], [40, 40]], [[60, 60], [99, 99]])
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
    # simulation for random distribution
    # random_loc = randomStoreLoc(cityMap, 10, False)
    # rand_markets = getMarkets(random_loc,"level4",50)
    # test = rand_markets[0]
    # print(test.getCost())
    #
    # print(getTotalProfit(rand_markets, cityResident))
    #
    #
    #
    #
    #
    # # simulation for even distribution
    # uniform_loc = randomStoreLoc(cityMap, 10, True)
    # for i in [10,20,30,40,50]:
    #     uni_markets = getMarkets(uniform_loc,"level3",i)
    #     print(getTotalProfit(uni_markets,cityResident))






if __name__ == '__main__':
    main()
#
# market1 = Market((3,4),"level2",5)
# lucy = Resident("median",(5,5))
# print(lucy.purchase(market1.sell_price,market1.location))
# store = (1,1)
# print(market1.sell_price)
# lucy = Resident(3,2)
# print(lucy.purchase(market1.price))


