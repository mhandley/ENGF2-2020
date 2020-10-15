# Step by step GCD computation for numbers 42 (=6*7) and 30 (=6*5)
a = 42
b = 30

# First, a > b, pick a
v = a - b     # v == 12
a = v

# Now, b > a, pick b
b = b - a     # b == 18

# Still, b > a, pick b
b = b - a     # b == 6

# Now, a > b, pick a
a = a - b     # a == 6

print(a)      # Now a == b so, we stop. GCD is in a, or, b.
