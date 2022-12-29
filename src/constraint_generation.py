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


def gen_constraints_PT(B, fields):
    # B is a set of raw tuples
    # S is the set of constraints
    S = set()
    # take it randomly or take the first one in b
    i = random.randint(0, len(fields) - 1)
    field = fields[i]
    for t in B:
        S.add(f"{field} != {t[i]}")

    return S

def gen_constraints_PF(B, fields):
    # B is a set of raw tuples
    # S is the set of constraints
    S = set()
    
    for t in B:
        for i, field in enumerate(fields):
            S.add(f"{field} != {t[i]}")
    
    return S


def constraint_generation(A, bpl, fields):
    for (b, pc, B) in A:
        if bpl == "PF":
            S = gen_constraints_PF(B, fields)
        elif bpl == "PT":
            S = gen_constraints_PT(B, fields)
