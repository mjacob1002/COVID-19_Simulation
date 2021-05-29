import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("Aggregates/StandardVax/ICU.csv")
df1 = pd.read_csv("Aggregates/SpreadingVax/ICU.csv")
df2 = pd.read_csv("Aggregates/AgeVax/ICU.csv")
df3 = pd.read_csv("Aggregates/MovementVax/ICU.csv")
plt.plot(df["Days"], df["mean"], "k-")
plt.fill_between(df["Days"], df["mean"]- df["MarginOfError"], df["mean"]+df["MarginOfError"])
plt.plot(df1["Days"], df1["mean"], 'r')
plt.fill_between(df1["Days"], df1["mean"] - df1["MarginOfError"], df1["mean"]+df1["MarginOfError"], color='green')
plt.plot(df2["Days"], df2["mean"], 'orange')
plt.fill_between(df2["Days"], df2["mean"] - df2["MarginOfError"], df2["mean"]+df2["MarginOfError"], color='pink')
plt.plot(df3["Days"], df3["mean"], 'brown')
plt.fill_between(df3["Days"], df3["mean"] - df3["MarginOfError"], df3["mean"]+df3["MarginOfError"], color='cyan')

plt.show()
print("plot shown")
for i in range(len(df)):
    print("[", df["LowerBound"].iloc[i], ", ", df["UpperBound"].iloc[i], "]")
