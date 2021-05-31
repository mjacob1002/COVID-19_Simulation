import os, sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parent_path = os.path.dirname(os.getcwd())
agg_path = parent_path + "/Aggregates"

# variable selection
compart = "ICU.csv"

# paths to all of the diff strategy V aggregates 
NoVax_path = agg_path + "/NoVax/" + compart
StdVax_path = agg_path + "/StandardVax/" + compart
AgeVax_path = agg_path + "/AgeVax/" + compart
Move_path = agg_path + "/MovementVax/" + compart
Spread_path = agg_path + "/SpreadingVax/" + compart

# dataframe for novax aggregate of vaccination
novax_v = pd.read_csv(NoVax_path, index_col=False)

# similar for the rest
stdvax_v = pd.read_csv(StdVax_path, index_col=False)
agevax_v = pd.read_csv(AgeVax_path, index_col=False)
movevax_v = pd.read_csv(Move_path, index_col=False)
spreadvax_v = pd.read_csv(Spread_path, index_col=False)

# marginal differences dataframes
marg_std = np.zeros(len(stdvax_v.index))

for i in range(1, len(marg_std)):
    marg_std[i] = stdvax_v['mean'].iloc[i] - novax_v['mean'].iloc[i]
print(marg_std)