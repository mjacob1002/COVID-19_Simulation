import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from matplotlib import pyplot as plt

class ModelFitting:

    def __init__(self):
        self.df = pd.read_csv("Approx_p0_vs_S(x)avg.csv")
        #print(df)
        self.p0 = self.df['p0'].to_numpy().reshape(-1,1)
        self.avg = self.df['Average of S(x)'].to_numpy().reshape(-1,1)
        #print(self.avg)
    
    def fit(self):
        x_train, xTest, y_train, y_test = train_test_split(self.p0, self.avg, test_size=0.2, random_state=0)
        reg = LinearRegression().fit(x_train, y_train)
        print("r^2: ", reg.score(x_train, y_train))
        print("Equation: y = ", reg.coef_, "x +", reg.intercept_)
        print("Accuracy test:")
        y_test = y_test.flatten()
        y_predict = reg.predict(xTest).flatten()
        errors = y_test - y_predict
        stacked = np.stack((y_test, y_predict, errors), axis=1)
        tempDF = pd.DataFrame(stacked, columns=["Y Actual", "Y Predict", "Error"])
        tempDF.to_csv("errors_mu_45_sigma_20_point_6.csv")
        print(tempDF)
    
    def plot(self):
        plt.scatter(self.df['p0'].to_numpy(), self.df["Average of S(x)"].to_numpy())

def main():
    testObj = ModelFitting()
    testObj.fit()

if __name__ == '__main__':
    main()
