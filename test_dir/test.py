def P_test(t, pc):
    test_1(t, pc)

def test_1(t, pc):  
    # LUOGO NASCITA
    if t.age == 50:
        pc += [('age', '==', 50)]
        
        # DATA ACCADIMENTO
        if t.zip_code <= 20000:
            pc += [('zip_code', '<=', 20000)]
        
        elif t.zip_code <= 40000:
            pc += [('zip_code', '<=', 40000)]
            pc += [('zip_code', '>=', 20000)]

        else:
            pc += [('zip_code', '>=', 40000)]

    else:
        pc += [('age', '!=', 50)]

        if t.zip_code <= 50000:
            pc += [('zip_code', '<=', 50000)]
        else:
            pc += [('zip_code', '>=', 50000)]