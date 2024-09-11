import pandas as pd
from Tester import TestQuestion

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

def find_m(n):
    m = n
    while True:
        for i in range(2, int(m**0.5) + 1):
            if m % i == 0 and is_prime(i) and is_prime(m//i):
                return (i, m//i)
        m += 1

def correct_encrypt(msg, pad):
    row, col = find_m(len(msg))
    res = [msg[i::col] for i in range(col)]
    res = map(lambda segment: segment + pad * (row -  len(segment)), res)
    return "".join(res)

# ========================================================================
if __name__ == "__main__":
    file = pd.read_csv("./2310-SUBS.csv")
    codes = file['Question 2: Q1B'][:10]
    BLANK = codes[7]
    inputs = [
        ('CS1010', 'S'),
        ('CS1010S is easy...', '!'),
        ('C ySi.1s.0 .1e!0a!Ss!', '!'),
        ('Cs! .0y0aS !i.S.1s1e!', '!'),
        ('C0Ssa.!S1  s.!10iey.!', '!'),
        ('SOMEThIng is N0T ok..? hAHa', '$')]
    answers = [correct_encrypt(*i) for i in inputs]

    tester = TestQuestion(codes, 'encrypt', inputs, answers)
    tester.setBlankTemplate(BLANK)
    tester.setFunctions({'is_prime':is_prime, 'find_m':find_m})

    tester.start()


