import pandas as pd
import numpy as np
import pyarrow

df_list = []
missing_files = []
num_files = 400

for i in range(1, num_files):
    filename = "../output/rejection/summary_stats/summary_stats_{}.feather".format(i)
    try:
        df = pd.read_feather(filename)
        df = df.reset_index(drop=True)
        df_list.append(df)
    except pyarrow.lib.ArrowIOError:
        missing_files.append(i)

sum_stats = pd.concat(df_list, axis=0).reset_index(drop=True)
sum_stats = sum_stats.sort_values(by="random_seed")

# Check everything look right
seeds = sum_stats["random_seed"]

difs = np.setdiff1d(np.arange(1,len(sum_stats)), np.array(seeds))

if len(missing_files) != 0:
    print("Warning: there are files missing in specified range")

if len(difs) != 0:
    print("Warning: np.setdiff1d suggests missing seeds")

sum_stats.to_csv("../output/summary_stats.csv", index=False)