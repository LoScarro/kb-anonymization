import logging
import anonypy
import pandas as pd

def is_concrete(field):
    return True


# Initialize PC_Buckets, a dictionary which groups tuples based on path conditions, mapping PC to a list of tuples which have that PC
def k_anonymization(PC_Buckets, sd, qi, k, bpl):
    logging.info("k-anonymization Module Starting")

    # Initialize A, a dataset holding intermediate k-anonymized groups
    A = set()
    # For each Bucket with (key, value) = (pc, B)
    for pc, B in PC_Buckets.items():
        # Invoke a k-anonymization algorithm on B and get its result 
        df = pd.DataFrame(data=B, columns=list(qi)+[sd])

        for name in (list(qi)+[sd]):
            df[name] = df[name].astype("category")

        p = anonypy.Preserver(df, qi, sd)
        B_anon = p.anonymize_k_anonymity(k)
        #   remove duplicates in B'
        # remove_duplicates(B_anon)
    
    
        for b in B_anon:
            # no field in b contain concrete values
            if bpl == "IT" and (len(b) <= 1 or not any(is_concrete(field) for field in b)):
                logging.error("Error: unsatisfiable case")
                continue
            
            A.add((b, pc, B))

    return A