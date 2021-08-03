import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("Aggregates/StandardVax/I.csv")
df1 = pd.read_csv("Aggregates/SpreadingVax/I.csv")
df2 = pd.read_csv("Aggregates/AgeVax/I.csv")
df3 = pd.read_csv("Aggregates/MovementVax/I.csv")
df4 = pd.read_csv("Aggregates/NoVax/I.csv")
plt.plot(df["Days"], df["mean"], "k-", label="Standard")
plt.fill_between(df["Days"], df["mean"]- df["MarginOfError"], df["mean"]+df["MarginOfError"])
plt.plot(df1["Days"], df1["mean"], 'r', label="Spreading")
plt.fill_between(df1["Days"], df1["mean"] - df1["MarginOfError"], df1["mean"]+df1["MarginOfError"], color='green')
plt.plot(df2["Days"], df2["mean"], 'orange', label="Age")
plt.fill_between(df2["Days"], df2["mean"] - df2["MarginOfError"], df2["mean"]+df2["MarginOfError"], color='pink')
plt.plot(df3["Days"], df3["mean"], 'brown', label='Movement')
plt.fill_between(df3["Days"], df3["mean"] - df3["MarginOfError"], df3["mean"]+df3["MarginOfError"], color='cyan')
plt.plot(df4["Days"], df4["mean"], label="NoVax")
plt.fill_between(df4["Days"], df4["LowerBound"], df4["UpperBound"], color="purple")
plt.legend()
plt.show()
print("plot shown")
for i in range(len(df)):
    print("[", df["LowerBound"].iloc[i], ", ", df["UpperBound"].iloc[i], "]")



# article to be read later
# https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-020-09826-8#Sec4