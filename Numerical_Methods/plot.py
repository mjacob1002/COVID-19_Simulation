import matplotlib.pyplot as plt
import pandas as pd
import sys 
# the regression slope
reg_m = 0.16196146
# the regression y-int
b = 0.0005

file = sys.argv[1]

df = pd.read_csv(file)
df["Avg of P(x)"] = df["Average of S(x)"]
df.plot(x="p0", y="Avg of P(x)")
plt.plot(df["p0"], reg_m*df["p0"]+b, color='r')
plt.xlabel("p0")
plt.ylabel("Average of P(x)")
plt.title("Relationship Between p0 and η")
plt.show()

print("Done")