# Construct constraints for various configurations

# For each {b, pc, B} in A:
#   if O == "P-F":
#     S = gen_constraints_PF(B)
#
#   elif O == "P-T":
#     S = gen_costraints_PT(B)
#
#   elif O == "I-T":
#     S = gen_costraints_IT(B, b)
#
#   else:
#     Output “Error: unimplemented option”
#     continue
#
#   S = S U pc

import random
import logging
from src.utility import is_concrete, first_concrete
from src.constraint_solver import gen_new_tuple
import re

def gen_constraints_IT(B, b, fields):
    # B is a set of raw tuples
    # b is a tuple that may has gen values or '-' or ','
    S = set()
    field = None

    # ensure no tuple repeat
    if all(is_concrete("", fld, value) for fld, value in b.items()):
        S = gen_constraints_PT(B)
        field = b[0] # first field of b

    else:
        field, idx = first_concrete(b) # first field in b containing a gen value or '-' or ','
        for t in B:
            S.add((field, "!=", t[idx]))
    
    # ensure some fields mantain their values
    # conc_field is the name of the column
    for conc_field in fields:
        if is_concrete("", conc_field, b[conc_field]) and conc_field != field:
            S.add((conc_field, "!=", b[conc_field]))

    return S

def gen_constraints_PT(B, fields):
    # B is a set of raw tuples
    # S is the set of constraints
    S = set()
    # take it randomly or take the first one in b
    i = random.randint(0, len(fields) - 2)
    field = fields[i]
    for t in B:
        S.add((field, "!=", t[i]))

    return S

def gen_constraints_PF(B, fields):
    # B is a set of raw tuples
    # S is the set of constraints
    S = set()
    
    for t in B:
        for i, field in enumerate(fields):
            S.add((field, "!=", t[i]))
    
    return S


def constraint_generation(A, bpl, fields, PC_map):
    R_out = []

    for (b, pc, B) in A:
        if bpl == "PF":
            S = gen_constraints_PF(B, fields)

        elif bpl == "PT":
            S = gen_constraints_PT(B, fields)

        elif bpl == "IT":
            S = gen_constraints_IT(B, b, fields)
        
        else:
            logging.error("Error: unimplemented option")
            continue
        
        S = S.union(PC_map[pc])

        # Invoke a constraint solver on S, and get its result r
        r = gen_new_tuple(S, fields) # finds a tuple which satisfy constraints
        # if a tuple r satisfy the constraints:
        R_out.append(r)
            
    return R_out