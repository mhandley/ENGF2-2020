def GCD(a,b):
    """Compute the GCD of two positive int."""
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

ax = 42                 
bx = 30                 
result = GCD(ax, bx) # Call the GCD function
print(result)  
