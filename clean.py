# script used for generating dbs

import numpy as np
import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=str, default=20)
    args = parser.parse_args()

    df = pd.read_csv("data/db_50000.csv", low_memory=False)
    df = df.sample(frac = 1)
    df = df.iloc[:int(args.rows)]
    df.to_csv(f"data/db_{args.rows}.csv", index = False, header=True)