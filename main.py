import argparse
from src import program_execution as pe
import numpy as np
import pandas as pd
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="data/in.csv")
    parser.add_argument('--output_file', type=str, default="data/out.csv")
    parser.add_argument('--k', type=int, default=2)
    parser.add_argument('--bpl', type=str, default="PT", help="Behaviour Preservation Level (PT) (PF) (IT)")
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='{levelname}:{message}', level=logging.INFO, style='{')  # output info on stdout
    
    R = pd.read_csv(args.input_file)

    PC_Buckets = pe.program_execution(R, args.k)
    print(PC_Buckets)

    return


if __name__ == "__main__":
    main()