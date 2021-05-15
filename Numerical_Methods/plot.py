import matplotlib.pyplot as plt
import pandas as pd
import sys 

file = sys.argv[1]

df = pd.read_csv(file)

df.plot(x="p0", y="Average of S(x)")
plt.show()

print("Done")