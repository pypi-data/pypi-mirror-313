from itertools import permutations

def cryptarithmetic():
    """

    
    Example:
    >>> from algoai import cryptarithmetic
    >>> cryptarithmetic()
    SEND = 9567
    MORE = 1085
    MONEY = 10652

    Code:
    -----
    def cryptarithmetic():
        letters = "SENDMORY"
        digits = range(10)

        for perm in permutations(digits, len(letters)):
            s, e, n, d, m, o, r, y = perm

            if s == 0 or m == 0:
                continue

            send = s * 1000 + e * 100 + n * 10 + d
            more = m * 1000 + o * 100 + r * 10 + e
            money = m * 10000 + o * 1000 + n * 100 + e * 10 + y

            if send + more == money:
                print("SEND =", send)
                print("MORE =", more)
                print("MONEY =", money)
                break
    """
    
    letters = "SENDMORY"
    digits = range(10)

    for perm in permutations(digits, len(letters)):
        s, e, n, d, m, o, r, y = perm

        if s == 0 or m == 0:
            continue

        send = s * 1000 + e * 100 + n * 10 + d
        more = m * 1000 + o * 100 + r * 10 + e
        money = m * 10000 + o * 1000 + n * 100 + e * 10 + y

        if send + more == money:
            print("SEND =", send)
            print("MORE =", more)
            print("MONEY =", money)
            break


