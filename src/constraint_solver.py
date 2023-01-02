import copy
import random

# transform a high level constraint in a z3 formula
def parseOp(possible_values, attr, op, val):
    if op == '==':
        possible_values[attr].add(val)
    elif op == '!=':
        possible_values[attr].remove(val)
    elif op == '>=':
        possible_values[attr] = set(filter(lambda x: x >= val, possible_values[attr]))
    elif op == '<=':
        possible_values[attr] = set(filter(lambda x: x <= val, possible_values[attr]))
    elif op == '>':
        possible_values[attr] = set(filter(lambda x: x > val, possible_values[attr]))
    elif op == '<':
        possible_values[attr] = set(filter(lambda x: x < val, possible_values[attr]))
    else:
        print('[!!] This operation ({}) is not allowed'.format(op))
        exit(1)


# add paths' constraints collected during the execution of the program
def set_constraints(S, all_constraints, possible_values):
    for (attr, op, val) in S:
        val = int(val)
        all_constraints.add(parseOp(possible_values, attr, op, val))


def get_possible_tuple(possible_values, fields, b):
    r = copy.deepcopy(b)
    for field in fields:
        r[field] = random.choice(tuple(possible_values[field]))
    return r

# collect all the constraints and try to derive a new tuple
def gen_new_tuple(S, fields, config_file, b, min_val, max_val):
    all_constraints = set()

    configs = [line.split() for line in open(config_file)]

    possible_values = {}
    for f in fields:
        possible_values[f] = set(range(min_val[f], max_val[f]+1)) 

    # collecting constraints
    set_constraints(S, all_constraints, possible_values)     # path-based
    set_constraints(configs, all_constraints, possible_values)     # path-based

    # get a tuple which satisfies all the constraints
    return get_possible_tuple(possible_values, fields, b)
