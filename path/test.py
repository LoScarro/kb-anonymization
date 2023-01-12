def P_test(t, pc):
    test_1(t, pc)
    test_2(t, pc)
    test_3(t, pc)
    test_4(t, pc)

##########
# TEST 1 #
##########

def test_1(t, pc):      
    # pay
    if t.job == "Transit Operator" or t.job == "TRANSIT OPERATOR":
        pc += [('job', '==', "Transit Operator")]
    else:
        pc += [('job', '!=', "Transit Operator")]

    if 320000 <= t.pay <= 540000:
        pc += [('pay', '<=', 540000)]
        pc += [('pay', '>', 320000)]
    
    elif 160000 <= t.pay <= 320000:
        pc += [('pay', '<=', 320000)]
        pc += [('pay', '>', 160000)]
    else:
        pc += [('pay', '<=', 160000)]

    
    
def test_2(t, pc):
    if t.job == "Special Nurse" or t.job == "SPECIAL NURSE":
        pc += [('job', '==', "Special Nurse")]
    else:
        pc += [('job', '!=', "Special Nurse")]
    
    if t.zip_code <= 20000:
            pc += [('zip_code', '<=', 20000)]
        
    elif t.zip_code <= 40000:
        pc += [('zip_code', '<=', 40000)]
        pc += [('zip_code', '>=', 20000)]
    else:
        pc += [('zip_code', '>=', 40000)]