import copy
import random
import logging 

# change the possible values for a field basing on the constraint
def apply_constraint(possible_values, field, op, val):
    if op == '==':
        possible_values[field].add(val)
    elif op == '!=':
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


# add paths' constraints collected during the execution of the program
def set_constraints(S, possible_values):
    for (field, op, val) in S:
        apply_constraint(possible_values, field, op, val)


def get_possible_tuple(possible_values, fields, b):
    r = copy.deepcopy(b)
    for field in fields:
        r[field] = random.choice(tuple(possible_values[field]))
    return r

# collect all the constraints and try to derive a new tuple
def gen_new_tuple(S, fields, config_file, b, min_val, max_val, categorical_values):

    configs = [line.split() for line in open(config_file)]
    configs = [(field, op, int(val)) for (field, op, val) in configs]

    possible_values = {}
    for f in fields:
        if f in min_val:
            possible_values[f] = set(range(min_val[f], max_val[f]+1)) 

    possible_values = possible_values | categorical_values
    # collecting constraints
    set_constraints(S, possible_values)     # path-based
    set_constraints(configs, possible_values)     # path-based

    # get a tuple which satisfies all the constraints
    return get_possible_tuple(possible_values, fields, b)
