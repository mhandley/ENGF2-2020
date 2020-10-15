import time

lst = []
count = 0
starttime = time.time()
print(0, 0)
while count < 10000000:
    lst.append(count)
    if count % 10000 == 0:
        now = time.time()
        print(now - starttime, count)
    count += 1
    
