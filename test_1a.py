import pandas as pd
from Tester import TestQuestion

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

def correct_find_m(n):
    m = n
    while True:
        for i in range(2, int(m**0.5) + 1):
            if m % i == 0 and is_prime(i) and is_prime(m//i):
                return (i, m//i)
        m += 1

if __name__ == "__main__":
    file = pd.read_csv("./2310-SUBS.csv")
    codes = file['Question 1: Q1A']
    BLANK = codes[278]
    special_inputs = [(0,), (1,), (2,), (3,)]
    inputs = [
        (4,),  (5,),  (6,),  (7,),  (8,),
        (13,), (15,), (17,), (22,), (25,),
        (26,), (27,), (31,), (32,), (38,),
        (42,), (46,), (49,), (50,), (52,),
        (59,), (75,), (77,), (83,), (84,),
        (85,), (95,), (97,), (100,)]
    answers = [correct_find_m(*i) for i in special_inputs + inputs]

    tester = TestQuestion(codes, 'find_m', special_inputs + inputs, answers)
    tester.setBlankTemplate(BLANK)
    tester.setFunctions({'is_prime':is_prime})

    tester.start()

    
    
