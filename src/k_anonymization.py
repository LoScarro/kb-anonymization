# Initialize A, a dataset holding intermediate k-anonymized groups
# 
# For each Bucket with (key, value) = (pc, B)
#   B' = Invoke a k-anonymization algorithm on B and get its result 
#   remove duplicates in B'
# 
#   For each tuple b ∈ B'
#     If O == "I-T":
#       If len(b) <= 1 or no field in b contain concrete values
#         Output “Error: unsatisfiable case”
#         continue
#     A.add({b, pc, B})