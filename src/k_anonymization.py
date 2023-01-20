import logging
from anonypy.anonypy import anonypy
import pandas as pd
from src.utility import is_concrete

# k-anonymization of a single Bucket which outputs non duplicate anonymized tuples, togheter with the pc and the original Bucket  
def k_anonymization(PC_Buckets, all_cols, sd, categorical, qi, k, bpl):
    logging.info("k-anonymization Module Starting")

    # Initialize A, a list holding intermediate k-anonymized groups
    A = []
    # For each Bucket with (key, value) = (pc, B)
    for pc, B in PC_Buckets.items():
        
        # Prepare anonypy dataframe
        df = pd.DataFrame(data=B, columns=all_cols)
        
        for name in categorical:
            if name not in all_cols: raise Exception(f"No column named {name}")
            df[name] = df[name].astype("category")

        # Invoke a k-anonymization algorithm on B and get its result 
        p = anonypy.Preserver(df, qi, sd)
        B_anon = p.anonymize_k_anonymity(k)

        # remove duplicates: this is a minimal k-anonymization
        for row in B_anon:
            del row['count']
    

        for b in B_anon:
            # no field in b contain concrete values
            if bpl == "IT" and (len(b) <= 1 or not any(is_concrete(field, value, sd) for field, value in b.items())):
                logging.info("Unsatisfiable case founded")
                continue
            else:
                for field, value in b.items():
                    # if is concrete and is not categorical, cast to int
                    if is_concrete(field, value, sd) and field not in categorical:
                        b[field] = int(value)

            A.append((b, pc, B))

    return A