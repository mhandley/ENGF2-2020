days = ["mon", "tues", "weds", "thurs", "FRIDAY!!!"]

#another list of days - careful here, just allocates 
#another name for the same list
moredays = days
# moredays is now ["mon", "tues", "weds", "thurs", "FRIDAY!!!"]

#calm down
moredays[4] = "fri"
# moredays is now ["mon", "tues", "weds", "thurs", "fri"]
# days is now ["mon", "tues", "weds", "thurs", "fri"]

yetmoredays = days.copy()   # an actual copy, not the original
yetmoredays[0] = "YAWN!"
# yetmoredays is now ["YAWN", "tues", "weds", "thurs", "fri"]
# days is still ["mon", "tues", "weds", "thurs", "fri"]

