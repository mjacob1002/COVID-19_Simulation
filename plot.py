import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("Aggregates/StandardVax/I.csv")
plt.plot(df["Days"], df["mean"], "k-")
plt.fill_between(df["Days"], df["mean"]- df["MarginOfError"], df["mean"]+df["MarginOfError"])
plt.show()
print("plot shown")
for i in range(len(df)):
    print("[", df["LowerBound"].iloc[i], ", ", df["UpperBound"].iloc[i], "]")
