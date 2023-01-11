import numpy as np
import pandas as pd

df = pd.read_csv("data/cleaned-salaries.csv", low_memory=False)
column_names = df.keys().values.tolist()
for col in column_names:
    df.drop(df[df[col] == "0"].index, inplace=True)

df.to_csv("data/sup-cleaned-salaries.csv", index = False, header=True)