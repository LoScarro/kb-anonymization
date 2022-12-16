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