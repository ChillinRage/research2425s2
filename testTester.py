from Tester import TestQuestion
import pandas as pd

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

if __name__ == "__main__":
    inputs = [
        ('CS1010', 'S'),
        ('CS1010S is easy...', '!'),
        ('C ySi.1s.0 .1e!0a!Ss!', '!'),
        ('Cs! .0y0aS !i.S.1s1e!', '!'),
        ('C0Ssa.!S1  s.!10iey.!', '!'),
        ('SOMEThIng is N0T ok..? hAHa', '$')
        ]

    answers = [
        'C0S110', 'C ySi.1s.0 .1e!0a!Ss!', 'Cs! .0y0aS !i.S.1s1e!',
        'C0Ssa.!S1  s.!10iey.!', 'CS1010S is easy...!!!', 'Ss O hMNAE0HTTah $Io$nk$g.$ .$i?$'   
        ]

    file = pd.read_csv("./2310-SUBS.csv")
    codes = file['Question 2: Q1B'][:20]

    main = TestQuestion(codes, 'encrypt', inputs, answers)
    main.setFunctions({'is_prime':is_prime, 'find_m':find_m})
    main.setBlankTemplate(codes[7])
    main.start()
