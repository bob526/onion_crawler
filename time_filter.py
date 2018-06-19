import datetime

print(datetime.datetime.now())

nowtime = datetime.datetime.now()
oneday = datetime.timedelta(days=1)
threeday = datetime.timedelta(days=3)
yesterday = nowtime - oneday
print(yesterday)

# I want user pass an datetime objest representing the last uptime
# And I compare the time with 'yesterday'
# Return true = still alive, false = down site

# Compare test 1
print(yesterday < nowtime)  #If nowtime = uptime, it should be true = still alive
print(yesterday < (nowtime-threeday)) # Should be false

def stillUpOrNot(lastUpTime):
    nowtime = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    yesterday = nowtime - oneday
    return (yesterday < lastUpTime)