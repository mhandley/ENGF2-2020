days = ["mon", "tues", "weds", "thurs", "fri"]

#I don't like mondays
del days[0]
# days is now ["tues", "weds", "thurs", "fri"]

#OK, add monday back
days.insert(0, "mon")
# days is now ["mon", "tues", "weds", "thurs", "fri"]

days[4] = "FRIDAY!!!"
# days is now ["mon", "tues", "weds", "thurs", "FRIDAY!!!"]

