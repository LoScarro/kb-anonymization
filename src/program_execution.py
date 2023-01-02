import copy
import logging
from test_dir import test as test


class PathCondition:
    def __init__(self, conditions):
        self.conditions = conditions
    
    def toStr(self):
        return (("".join(["".join(str(x)) for x in self.conditions])))

# Initialize PC_Buckets, a dictionary which groups tuples based on path conditions, mapping PC to a list of tuples which have that PC
def program_execution(R, k):
    logging.info("Program Execution Module Starting") # to verbose

    # fill PC_Buckets
    PC_Buckets = {}
    PC_map = {}     # map path condition in string format to list format
    for t in R.itertuples():
        # execute P with t and collect the path condition 
        pc = []
        test.P_test(t, pc)
        PC = PathCondition(pc)
        PC_str = PC.toStr()     # convert to string because PC is not hashable
        PC_map[PC_str] = pc     # map for future use
        if PC_str not in PC_Buckets:
            PC_Buckets[PC_str] = []
        PC_Buckets[PC_str].append(list(t[1:]))
    
    # remove buckets which have not at least k elements
    PC_Buckets_copy = copy.deepcopy(PC_Buckets)
    for PC_str, B in PC_Buckets_copy.items():
        if len(B) < k:
            del PC_Buckets[PC_str]    
            logging.info("Unsatisfiable case founded")

    return PC_Buckets, PC_map