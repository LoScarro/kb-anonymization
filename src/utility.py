def is_concrete(field, value, sd=""):
    if isinstance(value, int): return True # if is an integer is concrete
    # a value is concrete if not contains "-" or ","
    return (("-" not in value) and ("," not in value) and (field != sd))

# if there's no concrete value for any fields, it returns none
def first_concrete(b):
    for idx, (field, value) in enumerate(b.items()):
        if is_concrete(field, value):
            return field, idx
    return None