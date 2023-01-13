import multiprocessing
import os
import argparse
from multiprocessing.managers import DictProxy
from pathlib import Path

import copy
from src import program_execution as pe
from src import k_anonymization as ka
from src import constraint_generation as cg
import pandas as pd

from time import perf_counter

import plotly.graph_objects as px
import numpy

RESULTS_DIR_PATH: Path = ((Path(__file__).absolute().parent.parent).joinpath("results"))
METRICS = ["pe_time", "ka_time", "cg_time", "total_time", "output_rows"]
N_USED = [100, 1000, 10000, 50000]
BPL_USED = ["PT", "PF", "IT"]
K_USED = [2, 5]

def start_test(
    args: argparse.Namespace,
    all_results,
    runs: int = 2,
) -> None:

    print(f"\nStarting {runs} simulations with: input={args.input_file}, k={args.k}, bpl={args.bpl}", flush=True)

    sim_results = {}
    for metric in METRICS:
        sim_results[metric] = []
        
    for _ in range(runs):
        t0 = perf_counter()

        R = pd.read_csv(args.input_file)
        identifiers = args.identifiers_columns.split()
        categorical = args.categorical_columns.split()
        for field in identifiers:
            del R[field]
        possible_vals = {}
        for field in categorical:
            possible_vals[field] = set(R[field].tolist())
        all_cols = R.columns.values.tolist()
        non_sensitive = copy.deepcopy(all_cols)
        non_sensitive.remove(args.sensitive_column)

        t1 = perf_counter()
        PC_Buckets, PC_map = pe.program_execution(R, args.k)

        t2 = perf_counter()
        A = ka.k_anonymization(PC_Buckets, all_cols, args.sensitive_column, categorical, non_sensitive, args.k, args.bpl)

        t3 = perf_counter()
        R_out = cg.constraint_generation(A, args.bpl, non_sensitive, categorical, PC_map, args.config_file, possible_vals)
        
        t4 = perf_counter()

        sim_results["pe_time"].append(t2-t1)
        sim_results["ka_time"].append(t3-t2)
        sim_results["cg_time"].append(t4-t3)
        sim_results["total_time"].append(t4-t0)
        sim_results["output_rows"].append(len(R_out))
    
    avg_results = {}
    for metric in METRICS:
        avg = sum(sim_results[metric])/len(sim_results[metric])
        print(f"\n{runs} simulations with: input={args.input_file}, k={args.k}, bpl={args.bpl}", flush=True)
        print(f"Average of {metric} is: {avg}", flush=True)
        avg_results[metric] = avg
    
    # create a lock
    lock = multiprocessing.Lock()
    # acquire the lock
    lock.acquire()

    all_results[(args.n, args.bpl, args.k)] = avg_results

    # release the lock
    lock.release()

    return

if __name__ == "__main__":  # noqa: C901
    os.makedirs(RESULTS_DIR_PATH, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="data/db_100.csv")
    parser.add_argument('--output_file', type=str, default="data/out.csv")
    parser.add_argument('--k', type=int, default=2)
    parser.add_argument('--bpl', type=str, default="PF", help="Behaviour Preservation Level (PT) (PF) (IT)")
    parser.add_argument('--categorical_columns', type=str, default="job city_birth", help="Categorical Fields (separated by space)")
    parser.add_argument('--identifiers_columns', type=str, default="name", help="Identifiers Fields (separated by space)")
    parser.add_argument('--sensitive_column', type=str, default="disease")
    parser.add_argument('--config_file', type=str, default="config/basic.cfg")
    parser.add_argument("--verbose", default=False, action='store_true')

    args = parser.parse_args()

    manager = multiprocessing.Manager()
    processes: list[multiprocessing.Process] = []
    
    try:
        # dictionary of all results: keys are tuples (n, bpl, k) and values are dict of results
        all_results: dict[tuple[int, str, int], dict[str, list[int]]] = manager.dict()

        for n in N_USED[0:1]: #, 10000, 50000]:
            args.input_file = f"data/db_{n}.csv"
            args.n = n

            # results: DictProxy = manager.dict()  # type: ignore

            for bpl in BPL_USED:
                args.bpl = bpl

                for k in K_USED:
                    args.k = k
                    
                    if multiprocessing:
                        process = multiprocessing.Process(
                            target=start_test, args=(args, all_results)  # type: ignore
                        )

                        processes.append(process)
                        process.start()
                    
                    else: start_test(args, all_results)
                

            for process in processes:
                process.join()

        print(all_results)
        
        x = ["PF(k=2)", "PF(k=5)", "PT(k=2)", "PT(k=5)", "IT(k=2)", "IT(k=5)"]
        #x = ["(100, 'PF', 2)", "(100, 'PF', 2)", "(100, 'PF', 2)", "(100, 'PF', 2)", "(100, 'PF', 2)", "(100, 'PF', 2)"]
        
        plot = px.Figure(data=
        [px.Bar(
            name = f'n={n}',
            x = x,
            y = [all_results[(n, bpl, k)]['output_rows'] for bpl in ['PF','PT','IT'] for k in [2,5]]
        )
        for n in N_USED]
        )
                        
        plot.show()  


    except KeyboardInterrupt as e:
        for process in processes:
            process.kill()
        raise e
