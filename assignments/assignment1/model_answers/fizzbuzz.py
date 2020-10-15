for i in range(1,101):
    output = ""
    if i % 3 == 0:
        output = "Fizz"
    if i % 5 == 0:
        output += "Buzz"
    if output == "":
        output = str(i)
    print(output)
