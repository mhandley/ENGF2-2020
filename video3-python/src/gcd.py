def gcd(a, b):
    # a, b MUST be positive
    if not (a > 0 and b > 0):
        raise ArithmeticError("%s, %s: Must be positive int." % (a, b))
    while not a == b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a
