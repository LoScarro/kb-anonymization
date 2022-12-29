import logging
from anonypy.anonypy import anonypy
import pandas as pd

def is_concrete(sd, field, value):
    # a value is concrete if not contains "-" or ","
    return (("-" not in value) and ("," not in value) and (field != sd))

# Initialize PC_Buckets, a dictionary which groups tuples based on path conditions, mapping PC to a list of tuples which have that PC
def k_anonymization(PC_Buckets, all_cols, sd, qi, k, bpl):
    logging.info("k-anonymization Module Starting")

    # Initialize A, a dataset holding intermediate k-anonymized groups
    A = []
    # For each Bucket with (key, value) = (pc, B)
    for pc, B in PC_Buckets.items():
        # Invoke a k-anonymization algorithm on B and get its result 
        df = pd.DataFrame(data=B, columns=all_cols)

        categorical = set(("city_birth", "disease"))
        for name in categorical:
            df[name] = df[name].astype("category")
        
        p = anonypy.Preserver(df, qi, sd)
        B_anon = p.anonymize_k_anonymity(k=2)

        #   remove duplicates in B'
        for row in B_anon:
            del row['count']
    
        for b in B_anon:
            # no field in b contain concrete values
            if bpl == "IT" and (len(b) <= 1 or not any(is_concrete(sd, field, value) for field, value in b.items())):
                logging.error("Error: unsatisfiable case")
                continue
            print("aaaa")
            A.append((b, pc, B))

    return A