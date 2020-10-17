def GCD(a,b):
    """Compute the GCD of two positive int."""
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

# Test case for function
def test_euclid(): 
    ax = 42                 # Create test case 
    bx = 30                 # from simple example.
    r = GCD(ax,bx)          # Turn test print,
    assert r == 6           # into assert.
