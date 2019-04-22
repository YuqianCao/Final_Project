# Final_Project
IS590PR Spring 2019. Top-level repository for student project forks

The detailed instructions for the Final Projects will be in the course Moodle.

### Team Member:
Yuqian Cao (NetID: yuqianc3) 

### Monte Carlo Simulation Scenario:
There are many factors may influence the profit of a supermarket. For instance, the pricing, location, customer volume, hiring cost. Suppose there is a company that wants to start a supermarket chain in a city and they have already known the resident’s income level. This simulation could be used to help them decide the size, price level, location and how many supermarkets to open in this city to maximize the profit.

### Preconditions: 
1. In my simulation, the map of a city is in a rectangular shape. User can input the city's rows and columns to create a city map. 
2. We assume that each element in the map array has a corresponding resident. The income level of each household is demonstrate by the value of the element.   
    0: Low income level househol
    1: Average income level household
    2: High income level household
3. For each resident, they have a shopping budget which is related to their income. And for each market, it has a average selling price. Residents are willing to shop in the market only if the selling price is lower or equal to their budget.
4. For each resident, their maximum tolerance toward the distance to the market is determined by the size of the market. People can tolerate longer distance if the market is bigger.

### Hypotheses: 

1. The best size and amount of supermarkets to be started is related to the population and income level.
2. Making the markets evenly distributed throughout the city is more profitable.
