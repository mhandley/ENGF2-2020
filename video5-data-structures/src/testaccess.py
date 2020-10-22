import time
lst = []
for length in range(4000, 1000001, 10000):
    while len(lst) < length:
        lst.append(42)
    count = 0
    x = 0
    starttime = time.time()
    while count < 1000:
        x += lst[count]                 # read from beginning
        #x += lst[length//2 + count]    # read from middle
        #x += lst[length - (count+1)]   # read from end
        count += 1
    now = time.time()
    print(length, now - starttime)

