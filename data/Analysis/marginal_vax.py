import os, sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# set figure resoution
plt.figure(dpi=1200)


parent_path = os.path.dirname(os.getcwd())
agg_path = parent_path + "/Aggregates"

# save fig path
fig_path = "/Users/mathewjacob/Desktop/RxCOVea/Vaccine_Portion/Results/61days/Figs/"

# type of compartment
compart = "ICU.csv"

# paths to all of the diff strategy desired compartment aggregates 
NoVax_path = agg_path + "/NoVax/" + compart
StdVax_path = agg_path + "/StandardVax/" + compart
AgeVax_path = agg_path + "/AgeVax/" + compart
Move_path = agg_path + "/MovementVax/" + compart
Spread_path = agg_path + "/SpreadingVax/" + compart

NoVax_V = agg_path + "/NoVax/V.csv"
StdVax_V = agg_path + "/StandardVax/V.csv"
AgeVax_V = agg_path + "/AgeVax/V.csv"
Move_V = agg_path + "/MovementVax/V.csv"
Spread_V = agg_path + "/SpreadingVax/V.csv"

# dataframe for novax aggregate of desired compartment
novax = pd.read_csv(NoVax_path, index_col=False)

# similar for the rest
stdvax = pd.read_csv(StdVax_path, index_col=False)
agevax = pd.read_csv(AgeVax_path, index_col=False)
movevax = pd.read_csv(Move_path, index_col=False)
spreadvax = pd.read_csv(Spread_path, index_col=False)

# dataframes for the aggregate vaccinations
novax_v = pd.read_csv(NoVax_V, index_col=False)

# similar for the rest
stdvax_v = pd.read_csv(StdVax_V, index_col=False)
agevax_v = pd.read_csv(AgeVax_V, index_col=False)
movevax_v = pd.read_csv(Move_V, index_col=False)
spreadvax_v = pd.read_csv(Spread_V, index_col=False)


# marginal differences dataframes
marg_std = np.zeros(len(stdvax.index))
diff_v = np.zeros(len(stdvax.index))
diff_ICU = np.zeros(len(stdvax.index))

print(stdvax)
print(novax)


for i in range(1, len(marg_std)):
    diff_ICU[i] = spreadvax['mean'].iloc[i] - novax['mean'].iloc[i]
    diff_v[i] = spreadvax_v['mean'].iloc[i] - spreadvax_v['mean'].iloc[i-1]
    marg_std[i] = diff_ICU[i] / diff_v[i]

marg_std *= -1

plt.step(spreadvax_v['mean'].iloc[1:], (marg_std[1:]), where='pre')
plt.plot(spreadvax_v['mean'].iloc[1:], marg_std[1:], 'o--', color='grey', alpha=0.3)
plt.xlabel("Number of Vaccinations")
plt.ylabel("Marginal Reduction in Hospitalizations Per Vaccination")
plt.title("Marginal Benefit in Hospitalizations Per Vaccination - SpreadingVax")
plt.savefig(fig_path + "SpreadingVax_Marginal_Benefit_ICU.png")
plt.show()