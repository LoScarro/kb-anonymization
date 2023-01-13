import copy
import logging
from path import test as test


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

        PC_map[PC.toStr()] = pc     # map for future use

        # insert tuple in the bucket
        if PC.toStr() not in PC_Buckets:
            PC_Buckets[PC.toStr()] = []
        PC_Buckets[PC.toStr()].append(list(t[1:])) # do not consider index of the tuple
    
    # remove buckets which have not at least k elements
    PC_Buckets_copy = copy.deepcopy(PC_Buckets)
    for PC_str, B in PC_Buckets_copy.items():
        if len(B) < k:
            del PC_Buckets[PC_str]    
            logging.info("Unsatisfiable case founded")

    return PC_Buckets, PC_map