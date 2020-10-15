days = ["mon", "tues", "weds", "thurs", "fri"]

# iteration over a list using an index,
# print one day per line
for day_num in range(0, len(days)):
    print(days[day_num])

# native iteration over a list (more pythonic!)
# print one day per line
for day in days:
    print(day)
