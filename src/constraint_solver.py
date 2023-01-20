import copy
import random
import logging 

# change the possible values for a field basing on the constraint   
def apply_constraints(S, possible_values):
    for (field, op, val) in S:
        if op == '==':
            if val in possible_values[field]:
                possible_values[field] = {val} # the set becomes a single possible value
            else:
                possible_values[field] = {} # the set becomes empty: 2 disjoint conditions
        elif op == '!=':
            if val in possible_values[field]:
                possible_values[field].remove(val)
        elif op == '>=':
            possible_values[field] = set(filter(lambda x: x >= val, possible_values[field]))
        elif op == '<=':
            possible_values[field] = set(filter(lambda x: x <= val, possible_values[field]))
        elif op == '>':
            possible_values[field] = set(filter(lambda x: x > val, possible_values[field]))
        elif op == '<':
            possible_values[field] = set(filter(lambda x: x < val, possible_values[field]))
        else:
            raise Exception("Invalid Constraint Operator")


def get_possible_tuple(possible_values, fields, b):
    r = copy.deepcopy(b)
    for field in fields:
        # if there's not a possible value, the tuple can't be generated
        if not possible_values[field]: 
            logging.info(f"No possible value founded for the field {field}")
            return None
        r[field] = random.choice(tuple(possible_values[field]))
    return r

# collect all the constraints and try to derive a new tuple
def gen_new_tuple(S, PC, fields, config_file, b, min_val, max_val, categorical_values):

    configs = [line.split() for line in open(config_file)]
    configs = [(field, op, int(val)) for (field, op, val) in configs]

    possible_values = {}
    for f in fields:
        if f in min_val:
            possible_values[f] = set(range(min_val[f], max_val[f]+1)) 

    possible_values = possible_values | categorical_values
    
    apply_constraints(PC, possible_values) # based on path
    apply_constraints(S, possible_values) # based on bpl
    apply_constraints(configs, possible_values) # based on configs

    # get a tuple which satisfies all the constraints
    return get_possible_tuple(possible_values, fields, b)
