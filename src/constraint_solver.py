from z3 import *

# finds a tuple which satisfy constraints
    #    S is the set of constraints
    #    r is the tuple that satisfies the constraints

    #    Invoke a constraint solver on S, and get its result r
    #    r = solve(S)

    #     return r
    


# transform a high level constraint in a z3 formula
def parseOp(dict_z3, attr, op, val):
    if op == '==':
        return (dict_z3[attr] == val)
    elif op == '!=':
        return (dict_z3[attr] != val)
    elif op == '>=':
        return (dict_z3[attr] >= val)
    elif op == '<=':
        return (dict_z3[attr] <= val)
    elif op == '>':
        return (dict_z3[attr] > val)
    elif op == '<':
        return (dict_z3[attr] < val)
    else:
        print('[!!] This operation ({}) is not allowed'.format(op))
        exit(1)


# add constraints about ranges of attributes (after have seen the dataset and the test program)
def add_range_constraints(solver, dict_z3, S):
    for conf in S:
        if conf.startswith('#'):
            # constraints which involve 2 fields
            arr = conf[1:].split(' ')
            solver.add(parseOp(dict_z3, arr[0], arr[1], dict_z3[arr[2]]))

        else:
            # range constraints of a single field
            field, constraints = conf.split(':')
            lst = constraints.split(',')
            if len(lst) == 1:   # all constraints are in AND
                ops_vals = lst[0].split(' ')
                for i in range(0, len(ops_vals), 2):
                    op = ops_vals[i]
                    val = int(ops_vals[i + 1])
                    solver.add(parseOp(dict_z3, field, op, val))

            else:
                ors = []
                for or_c in lst:
                    ands = []
                    ops_vals = or_c.split(' ')
                    for i in range(0, len(ops_vals), 2):
                        op = ops_vals[i]
                        val = int(ops_vals[i + 1])
                        ands += [parseOp(dict_z3, field, op, val)]

                    if len(ands) == 1:
                        ors += [ands[0]]  # a set of OR conditions

                    else:
                        ors += [And(ands)]  # a set of OR of ANDs conditions

                solver.add(Or(ors))


# add paths' constraints collected during the execution of the program
def set_constraints(S, solver, dict_z3):
    for (attr, op, val) in S:
        val = int(val)
        solver.add(parseOp(dict_z3, attr, op, val))


# convert the Z3 model into a tuple (== row in the released dataset)
def z3model2row(model, dict_z3):
    row = {}
    for k, v in dict_z3.items():
        if model[v] is not None:
            row[k] = model[v].as_long()
    return row


# collect all the constraints and try to derive a new tuple
def gen_new_tuple(S, fields, config_file):
    # Z3 variables and solver
    solver = Solver()

    configs = [line.split() for line in open(config_file)]

    dict_z3 = {}
    for f in fields:
        dict_z3[f] = Int(f)     #! not all values are integers

    # collecting constraints
    # add_range_constraints(solver, dict_z3, S)  # range-based
    set_constraints(S, solver, dict_z3)     # path-based
    set_constraints(configs, solver, dict_z3)     # path-based

    # try to solve the equation
    if solver.check() == sat:
        model = solver.model()
        return z3model2row(model, dict_z3)

    return None
