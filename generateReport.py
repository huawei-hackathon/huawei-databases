from hctools import users, announcements, bluetooth, healthInfo, reports
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from uuid import uuid4
from numpy.random import rand, normal
from random import choice
from progress.bar import Bar

def randrange(low, high):
    tx = rand()
    return low + tx * (high-low)

''' CREATE CAREGIVER '''
caregiverUserId = users.createCaregiver('Demonstration User', 'Nullpassword', f'demo {uuid4()}')['caregiverUserId']
print(f"caregiverUserId: {caregiverUserId}")

''' CREATE ELDERLY '''
elderlyUserId = users.createElderly('Demonstration Elderly', 78, caregiverUserId, 170, 65, 22.49, 'male')['userId']
print(f"elderlyUserId: {elderlyUserId}")

''' REPORT '''
reportUUID = uuid4()
reports.generateReport(reportUUID, elderlyUserId)
print("REPORT URL: ", f'http://119.13.104.214:80/getReport/{reportUUID}')

''' GENERATING HEALTH SIGNALS '''
now = datetime.now()
initDate = datetime(now.year, now.month, 1, 0, 0, 0)
endDate = datetime(now.year, now.month, 1, 0, 0, 0) + relativedelta(months = 1) - timedelta (seconds=1)
print("GENERATING HEALTH DATA")

bar = Bar("Processing...", max=31)
day = 1
while initDate < endDate:
    ''' CREATE SQL UPDATES '''
    timestr = (initDate+ timedelta(seconds = randrange(0, 7200))).strftime("%Y-%m-%d, %H:%M:%S")
    healthInfo.updateHealthInformation('heartRate', elderlyUserId, randrange(70, 81), timestr)
    healthInfo.updateHealthInformation('stepAsymmetry', elderlyUserId, randrange(1,6), timestr)
    if initDate.hour == 9:
        healthInfo.updateHealthInformation('sleepSeconds', elderlyUserId, randrange(6*3600, 8*3600), timestr)
    
    ''' STEP COUNT '''
    hour = [0, 3, 6, 9, 12, 15, 18, 21]
    low = [0, 0, 0, 100, 400, 600, 800, 1000]
    high = [0, 5, 10, 200, 600, 800, 900, 1250]
    ind = hour.index(initDate.hour)
    healthInfo.updateHealthInformation('stepCount', elderlyUserId, randrange(low[ind], high[ind]), timestr)
    
    ''' UPDATE DATE AND PROGRESS BAR'''
    initDate = initDate + timedelta(hours=3)
    if initDate.day > day:
        day += 1
        bar.next()
print()
print("HEALTH DATA COMPLETE")

''' GENERATE BLUETOOTH FOR ROOMS '''
initDate = datetime(now.year, now.month, 1, 0, 0, 0)
endDate = datetime(now.year, now.month, 1, 0, 0, 0) + relativedelta(months = 1) - timedelta (seconds=1)
ROOM = 'Bedroom'
roomlist = ['Outside', 'Living Room', 'Bedroom', 'Bathroom', 'Kitchen']

print("GENERATING BLUETOOTH ROOM DATA")
bar = Bar("Processing...", max=31)
day = 1
cooldown = False

while initDate < endDate:
    if initDate.day > day:
        day += 1
        bar.next()
        cooldown = False

    initDate += timedelta(minutes = normal(60, 10**2), seconds = 1)
    ''' GO TOILET '''
    if randrange(1,10) <= 5:
        timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
        bluetooth.locationUpdate(elderlyUserId, "Bathroom", timestr)
        initDate += timedelta(minutes = randrange(4, 8))
        timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
        bluetooth.locationUpdate(elderlyUserId, ROOM, timestr)
        continue

    ''' SLEEP ''' 
    if initDate.hour >= 22 or initDate.hour < 6:
        if ROOM != 'Bedroom':
            timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
            bluetooth.locationUpdate(elderlyUserId, "Bedroom", timestr)
            ROOM = "Bedroom"
        initDate = initDate + timedelta(minutes = normal(640, 30), seconds=1)
        continue
    
    ''' TIME TO GO OUT '''
    if initDate.hour >= 11 and initDate.hour <= 19 and not cooldown:
        if randrange(1,12) <= 4:
            timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
            bluetooth.locationUpdate(elderlyUserId, "Outside", timestr)
            initDate += timedelta(minutes = normal(120, 100), seconds=1)
            timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
            bluetooth.locationUpdate(elderlyUserId, "Living Room", timestr)
            ROOM = "Living Room"
            cooldown = True
            continue

    ''' RANDOM ROOM CHANGE '''
    if randrange(1,8) <= 7:
        rooms = ['Living Room', 'Living Room', 'Living Room', 'Kitchen', 'Kitchen', 'Bedroom', 'Kitchen']
        ''' REDUCE CHANCE OF GOING TO BEDROOM '''
        rooms = [i for i in rooms if i != ROOM]
        #print(rooms)
        target = choice(rooms)
        timestr = initDate.strftime("%Y-%m-%d, %H:%M:%S")
        bluetooth.locationUpdate(elderlyUserId, target, timestr)
        ROOM = target

print()
print("BLUETOOTH ROOM DATA COMPLETE")
