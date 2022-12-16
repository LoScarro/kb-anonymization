import argparse
from src import program_execution as pe
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="data/in.csv")
    parser.add_argument('--output_file', type=str, default="data/out.csv")
    parser.add_argument('--k', type=int)
    parser.add_argument('--bpl', type=str, default="PT", help="Behaviour Preservation Level (PT) (PF) (IT)")
    args = parser.parse_args()

    R = pd.read_csv(args.input_file)

    pe.program_execution(R, args.k)

    return


if __name__ == "__main__":
    main()