import argparse
from src import program_execution as pe
from src import k_anonymization as ka
import numpy as np
import pandas as pd
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="data/in.csv")
    parser.add_argument('--output_file', type=str, default="data/out.csv")
    parser.add_argument('--k', type=int, default=2)
    parser.add_argument('--bpl', type=str, default="PT", help="Behaviour Preservation Level (PT) (PF) (IT)")
    parser.add_argument('--sensitive_column', type=str, default="disease")
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='{levelname}:{message}', level=logging.INFO, style='{')  # output info on stdout
    
    R = pd.read_csv(args.input_file)

    sensitive = {args.sensitive_column}
    all_cols = set(R.columns.values.tolist())
    non_sensitive = all_cols - sensitive

    PC_Buckets = pe.program_execution(R, args.k)
    logging.info("Buckets Created:" + str(PC_Buckets))

    A = ka.k_anonymization(PC_Buckets, args.sensitive_column, list(non_sensitive), args.k, args.bpl)

    return


if __name__ == "__main__":
    main()