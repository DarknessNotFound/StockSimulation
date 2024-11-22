from random import normalvariate
from math import sqrt
from copy import deepcopy
import matplotlib.pyplot as plt

TIME_STEP = 1/365
TIME_STEP_SQRT = sqrt(TIME_STEP)

class stock():
    def __init__(self, price: float = 1, volitility: float = 0, free_market_manipulation: float = 0, moving_avg_length: int = 5) -> None:
        self.s = price
        self.v = volitility
        self.fmm = free_market_manipulation
        self.moving_mean_r = price
        self.mmr_length = moving_avg_length
        self.hist = [price]
    
    def __str__(self):
        return f"${self.s:.3f} -- {self.g*100:.1f}% expected growth -- {self.v*100:.1f}% volitility"
    
    def price_str(self):
        return f"${self.s:.3f}"
    
    def total_growth(self):
        return ((self.s - self.hist[0]) / self.hist[0])*100
    
    def step(self):
        self.s = calc_time_step(self.s, self.moving_mean_r, self.v, self.fmm)
        if self.s < 0:
            self.s = 0
        self.hist.append(self.s)
        self.update_moving_mean()
    
    def update_moving_mean(self):
        num_hist = len(self.hist)
        if num_hist > self.mmr_length:
            num_hist = self.mmr_length
        
        sum = 0
        for i in range(num_hist-1):
            p = self.hist[-1*(i+2)]
            c = self.hist[-1*(i+1)]
            sum += (c-p)/p
        self.moving_mean_r = sum / num_hist
    
    def graph_hist(self):
        plt.plot(self.hist)

class market():
    def __init__(self) -> None:
        pass

def calc_time_step(s: float, mu: float, v: float, fmm: float = 0) -> float:
    """Calculates a single time step for the stock price.

    Args:
        s (float): Current Stock price [0, inf]
        mu (float): mean of daily returns
        v (float): Volitility, [-2, 2]
        ffm (float): Free Market Manipulation, adjust the mean of the normal distrubtion by an amount nudging the model towards growth or decay.

    Returns:
        float: New Price
    """
    return s * (1+(mu*TIME_STEP)+(v*normalvariate(0+fmm, 1)*TIME_STEP_SQRT))


def main():
    NUM_YEARS = 10
    manipulator = 0.0
    volitility = 0.2
    base_market = {
        "AA" : stock(10.00, volitility, manipulator, 3),
        "AB" : stock(10.00, volitility, -manipulator, 3),
        "BA" : stock(10.00, volitility, manipulator, 5),
        "BB" : stock(10.00, volitility, -manipulator, 5),
        "CA" : stock(10.00, volitility, manipulator, 10),
        "CB" : stock(10.00, volitility, -manipulator, 10),
        "DA" : stock(10.00, volitility, manipulator, 20),
        "DB" : stock(10.00, volitility, -manipulator, 20),
    }
    keys = base_market.keys()

    market_growth = {}
    for k in keys:
        market_growth[k] = []

    num_iters = 1000
    for j in range(num_iters):
        print(f"Progress: {(j/num_iters)*100:.1f}%               ", end='\r')
        market_j = {}
        for k in keys:
            market_j[k] = deepcopy(base_market[k])

        for i in range(int(365*NUM_YEARS*24)):
            for k in keys:
                market_j[k].step()
        
        for k in keys:
            market_growth[k].append(market_j[k].total_growth())
    print(f"Progress: 100.0%")
    print("Mean Total Growth")
    for k in keys:
        sum = 0
        for mg in market_growth[k]:
            sum += mg
        print(f"\t{k}: {(sum / len(market_growth[k])):.2f}%")

    # fig, axes = plt.subplots(ncols=2, nrows=int(len(keys)//2))
    # counter = 0
    # for k in keys:
    #     axes[counter // 2, counter % 2].plot(market[k].hist)
    #     counter += 1
    # plt.show()
    #print(calc_time_step(1, 0.2, .3) - 1)

if __name__ == "__main__":
    main()