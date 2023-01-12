import numpy as np
import pandas as pd

df = pd.read_csv("data/db_50000.csv", low_memory=False)
df = df.sample(frac = 1)
df = df.iloc[:100]
df.to_csv("data/db_100.csv", index = False, header=True)