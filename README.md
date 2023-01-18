# kb-anonymization - DPP project
Authors: Lorenzo La Corte & Davide Scarrà

# usage
for install dependecies: make install
for executing main: make main dataset='value' bpl='value'
for executing statistics on few datasets: make test-partial
for executing statistics on all datasets: make test-full
for deleting output files: make clean

# description
main.py consists in only one execution of the algorithm.
statistics.py consists in multiple executions of the algorithm on selected datasets and the generation of the statistics.
Statistics are gathered and saved in /results and they involve:
    - total time
    - time for every module
        - program_execution
        - k_anonymization
        - constraint_generation (which also contains the generation of the new tuple)
    - number of rows in output
For the k-anonymity we use the k-anonymity library **anonypy**, k value is set to 2 by default in main.py and to [2,5] in statistics.py.