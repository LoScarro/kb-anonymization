import argparse
import copy
from src import program_execution as pe
from src import k_anonymization as ka
from src import constraint_generation as cg
import numpy as np
import pandas as pd
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="data/categorical.csv")
    parser.add_argument('--output_file', type=str, default="data/out.csv")
    parser.add_argument('--k', type=int, default=2)
    parser.add_argument('--bpl', type=str, default="PF", help="Behaviour Preservation Level (PT) (PF) (IT)")
    parser.add_argument('--categorical_columns', type=str, default="city_birth", help="Categorical Fields (separated by space)")
    parser.add_argument('--sensitive_column', type=str, default="disease")
    parser.add_argument('--config_file', type=str, default="config/basic.cfg")
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='{levelname}:{message}', level=logging.INFO, style='{')  # output info on stdout
    
    R = pd.read_csv(args.input_file)

    all_cols = R.columns.values.tolist()
    non_sensitive = copy.deepcopy(all_cols)
    non_sensitive.remove(args.sensitive_column)

    # make a list out of categorical cols
    categorical = args.categorical_columns.split()

    # take all possible values for each categorical field in the bucket
    possible_vals = {}
    for field in categorical:
        possible_vals[field] = set(R[field].tolist())

    PC_Buckets, PC_map = pe.program_execution(R, args.k)

    A = ka.k_anonymization(PC_Buckets, all_cols, args.sensitive_column, categorical, non_sensitive, args.k, args.bpl)

    R_out = cg.constraint_generation(A, args.bpl, non_sensitive, categorical, PC_map, args.config_file, possible_vals)
    
    # from dictionary to output file
    df = pd.DataFrame.from_dict(R_out)
    df.to_csv(args.output_file, index = False, header=True)
    
    return


if __name__ == "__main__":
    main()