import time
lst = []
count = 0
while count < 10000000: #create a long list
    lst.append(count)
    count += 1

starttime = time.time()
count = 0
while count < 10000000: #delete all items, one by one
    lst.pop(0)  # delete first item
    if count % 10000 == 0:
        now = time.time()
        print(now - starttime, count)
    count += 1
