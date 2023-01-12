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

RESULTS_DIR_PATH: Path = ((Path(__file__).absolute().parent.parent).joinpath("results"))
METRICS = ["pe_time", "ka_time", "cg_time", "total_time", "output_rows"]

def start_test(
    args: argparse.Namespace,
    sim_results,
    all_resuls,
    runs: int = 3,
) -> None:

    print(f"\nStarting {runs} simulations with: input={args.input_file}, k={args.k}, bpl={args.bpl}", flush=True)

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
    
    for metric in METRICS:
        print(f"\n{runs} simulations with: input={args.input_file}, k={args.k}, bpl={args.bpl}", flush=True)
        print(f"Average of {metric} is: {sum(sim_results[metric])/len(sim_results[metric])}", flush=True)
    
    # create a lock
    lock = multiprocessing.Lock()
    # acquire the lock
    lock.acquire()

    all_results[(args.n, args.bpl, args.k)] = sim_results

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

        for n in [100]: #, 10000, 50000]:
            args.input_file = f"data/db_{n}.csv"
            args.n = n

            # results: DictProxy = manager.dict()  # type: ignore

            for bpl in ["PT", "PF", "IT"]:
                args.bpl = bpl

                for k in [2,5]:
                    args.k = k

                    sim_results = {}
                    for metric in METRICS:
                        sim_results[metric] = []
                    
                    if multiprocessing:
                        process = multiprocessing.Process(
                            target=start_test, args=(args, sim_results, all_results)  # type: ignore
                        )

                        processes.append(process)
                        process.start()
                    
                    else: start_test(args, sim_results, all_results)
                

            for process in processes:
                process.join()

        print(all_results)
        print(all_results[100, 'IT', 2])


    except KeyboardInterrupt as e:
        for process in processes:
            process.kill()
        raise e
