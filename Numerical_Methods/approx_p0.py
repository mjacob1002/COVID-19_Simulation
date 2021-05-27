""" This file approximates the graph of different p0 values vs the average value of S(x), 
where S(x) = p0 / (1+exp(-(x-mu - stnd))), where x is the input age pulled from a normal distribution, mu is the 
mean of that normal distribution, and stnd is the standard deviation."
"""
# imports
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# introduce a truncated normal distribution
from scipy.stats import truncnorm

# approximated loosely from https://www.kff.org/other/state-indicator/distribution-by-age/?dataView=0&currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
mu = 45
sigma = 20.6

# defined function from here: https://stackoverflow.com/questions/36894191/how-to-get-a-normal-distribution-within-a-range-in-numpy
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

# the S(x) function, given a particular p0 and input age
def S(p0, x):
    return p0/(1+math.exp(-(x-mu-sigma)))

# computes the average of all values in numTrials used as inputs for S(x)
def average(p0, trials):
    sum = 0
    size = len(trials)
    for num in trials:
        if num < 0:
            raise ValueError
        output = S(p0, num)
        sum += output
    # return the average
    return sum / size

def main():
    numVals = 1001
    numP0 = np.linspace(0, 1, numVals)
    averages = np.zeros(numVals)
    # the number of generated values for the ages
    numTrials = 10000
    # truncated normal distribution instance
    distro = get_truncated_normal(mean=mu, sd=sigma, low=0, upp=math.inf)
    # get all of the average values
    for i, num in enumerate(numP0):
        trials = distro.rvs(numTrials)
        #trials = np.random.normal(mu, sigma, numTrials)
        averages[i] = average(num, trials)
    
    # create a pandas dataframe
    df = pd.DataFrame({'p0': numP0, 'Average of S(x)':averages})
    df.to_csv("Approx_p0_vs_S(x)avg.csv", index=False)

    plt.plot(numP0, averages, label="Average of S(x) function when applied to normal distribution")
    plt.xlabel("p0 value")
    plt.ylabel("Average of S(x)")
    plt.show()

if __name__ == '__main__':
    main()
    


