import logging
from tests import test as test

# Initialize PC_Buckets, a dictionary which groups tuples based on path conditions, mapping PC to a list of tuples which have that PC
def program_execution(R, k):
    logging.info("Program Execution Module Starting") # to verbose

    # FILL PC_Buckets
    
    for t in R.itertuples():
        print(t.age)
        pc = []
        test.P_test(t, pc)

        print(pc)



    #   pc = execute P with t and collect the path condition 
    #   If PC_Buckets does not contains pc
    #     PC_Buckets[pc] = []
    #   PC_Buckets[pc].append(t)
    #   
    # For each Bucket with (key, value) = (pc, B)
    #   if len(B) < k:
    #     del PC_Bucket[pc]    
    #     output “Error: unsatisfiable case” and continue


    return