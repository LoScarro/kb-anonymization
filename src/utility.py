def is_concrete(sd, field, value):
    # a value is concrete if not contains "-" or ","
    return (("-" not in value) and ("," not in value) and (field != sd))

# if there's no concrete value for any fields, it returns none
def first_concrete(b):
    for idx, (field, value) in enumerate(b.items()):
        if is_concrete("", field, value):
            return field, idx
    return None