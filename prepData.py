import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import glob

# path to where the CSV files wanted are. Change for different vaccination strategies tested

# path where the aggregated data for each compartment will be saved as csv files
# change this path depending on the vaccination strategy being tested


def getCSVFiles(simType):
    csvToDF = []
    path = "/Users/mathewjacob/Desktop/RxCOVea/Vaccine_Portion/Outputs/" + simType + "/*.csv"
    for fname in glob.glob(path):
        df = pd.read_csv(fname)
        csvToDF.append(df)
        print(fname)
    return csvToDF

# feed in a list of dataframes, then create a csv file containing all the susceptibles each from every run, E, I, etc.
def aggregateFiles(data: list):
    S = pd.DataFrame()
    E = pd.DataFrame()
    I = pd.DataFrame()
    L = pd.DataFrame()
    ICU = pd.DataFrame()
    R = pd.DataFrame()
    D = pd.DataFrame()
    V = pd.DataFrame()
    tempList = [S, E, I, L, ICU, R, D, V]
    # add the days column to all of the dataframes
    for i, df in enumerate(tempList):
        tempList[i]["Days"] = data[0]["Days"]
    # add all the susceptible runs to the S dataframe
    for i, df in enumerate(data):
        colTitle = "Run " + str(i+1)
        tempList[0][colTitle] = df["Susceptible"]
        tempList[1][colTitle] = df["Exposed"]
        tempList[2][colTitle] = df["Infectious"]
        tempList[3][colTitle] = df["Lag"]
        tempList[4][colTitle] = df["ICU"]
        tempList[5][colTitle] = df["Recovered"]
        tempList[6][colTitle] = df["Dead"]
        tempList[7][colTitle] = df["Vaccinated"]
    # calculate the mean at each time step for the aggregate data
    for i, df in enumerate(tempList):
        tempList[i]['mean'] = df.iloc[:, 1:305].mean(axis=1)
    return tempList

def testSlicing(df: pd.DataFrame):
    df['mean'] = df.iloc[:, 1:305].mean(axis=1)
    print(df)

def saveAggs(aggs: list, simType, columns=["S", "E", "I", "L", "ICU", "R", "D", "V"]):
    # make sure correct number of names for dataframes
    assert len(aggs) == len(columns)
    savePath = "/Users/mathewjacob/Desktop/RxCOVea/Vaccine_Portion/Aggregates/" + simType
    for i, df in enumerate(aggs):
        fname = savePath + "/" + columns[i] + ".csv"
        df.to_csv(fname)

# plots a boxplot at each day
def plot(data: pd.DataFrame):
    print(data.head())
    #plt.boxplot(data.iloc[:, 1:], positions=data["Days"])
    #plt.xlabel("Days")
    #plt.ylabel("Vaccinated")
    data.plot.line("Days")
    #plt.title("ICU Hospitalizaitons")
    plt.show()




# main function when running prepData
def main(simType):
    # get the data from csv files, convert to dataframe, and return a list of them
    data = getCSVFiles(simType)
    # aggregate the data for each compartment and return a list of dataframes
    aggData = aggregateFiles(data)
    plot(aggData[4])
    # save the aggregate data as csv files in desired location, determined by savePath variable
    saveAggs(aggData, simType)



    


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Pass in simType")
        exit(1)
    
    main(sys.argv[1])
