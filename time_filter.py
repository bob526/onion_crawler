import datetime

# I want user pass an datetime objest representing the last uptime
# And I compare the time with 'yesterday'
# Return true = still alive, false = down site


def stillUpOrNot(lastUpTime):
    '''
    Parameter: lastUpTime should be a datetime.datetime object.
    It will reture True = the website is working, False = the website is down
    '''
    nowtime = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    yesterday = nowtime - oneday
    return (yesterday < lastUpTime)