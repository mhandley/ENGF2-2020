days = ["mon", "tues", "weds", "thurs", "fri"]

#how many weekdays are there?
count = len(days)

#what's the second day of the week?
day2 = days[2]  # "weds"

#ooops, indices start at zero
#what's the second day of the week?
day2 = days[1]  # "tues"

#add the weekend
days.append("sat")
days.append("sun")  
# days is now ["mon", "tues", "weds", "thurs", "fri", "sat", "sun"]
