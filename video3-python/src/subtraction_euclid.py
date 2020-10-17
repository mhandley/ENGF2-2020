# Step by step GCD computation for numbers 42 (=6*7) and 30 (=6*5)
a = 42
b = 30

while a != b:
    if a > b:
        a = a - b
    else:
        b = b - a
        
print(a)      # Now a == b so, we stop. GCD is in a, or, b.
