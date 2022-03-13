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

def generateAnomaly(heartRate, sleepSeconds, stepAsymmetry, stepCount):
    ''' CREATE CAREGIVER '''
    caregiverUserId = users.createCaregiver('Demonstration User', 'Nullpassword', f'{uuid4}')['caregiverUserId']
    #caregiverUserId = users.createCaregiver('Demonstration User', 'Nullpassword', 'ElizabethKhua69')['caregiverUserId']
    print(f"caregiverUserId: {caregiverUserId}")

    ''' CREATE ELDERLY '''
    elderlyUserId = users.createElderly('Cedric Khua', 78, caregiverUserId, 170, 65, 22.49, 'male')['userId']
    print(f"elderlyUserId: {elderlyUserId}")

    ''' GENERATING HEALTH SIGNALS '''
    now = datetime.now()
    endDate = datetime(now.year, now.month, now.day, 23, 59, 59)
    initDate = endDate- relativedelta(months=1, seconds=-1)
    print(initDate, endDate)
    print("GENERATING HEALTH DATA")

    bar = Bar("Processing...", max=31)
    day = 1
    heartRateAvg = 70
    daySteps = 0
    while initDate < endDate:
        ''' CREATE SQL UPDATES '''
        timestr = (initDate+ timedelta(seconds = randrange(50,60))).strftime("%Y-%m-%d, %H:%M:%S")
        if not heartRate:
            healthInfo.updateHealthInformation('heartRate', elderlyUserId, normal(heartRateAvg,5), timestr)
        else:
            # INSERT HEART RATE ANOMALY AFTER DAY 20
            if initDate.day == 20 and initDate.hour == 17:
                healthInfo.updateHealthInformation('heartRate', elderlyUserId, normal(heartRateAvg+30,1), timestr)
            else:
                healthInfo.updateHealthInformation('heartRate', elderlyUserId, normal(heartRateAvg,5), timestr)

        #healthInfo.updateHealthInformation('stepAsymmetry', elderlyUserId, normal(4,0.5), timestr)
        #healthInfo.updateHealthInformation('sleepSeconds', elderlyUserId, normal(7*3600, 1800), timestr)
        
        ''' STEP COUNT '''
        if not stepCount:
            ''' No Anomaly '''
            if initDate.hour == 0:
                daySteps = 0 # Resets day steps
            if initDate.hour == 12:
                daySteps += 500
            if initDate.hour == 18:
                daySteps += 1000
            daySteps += normal(200,10)
            healthInfo.updateHealthInformation('stepCount', elderlyUserId, daySteps, timestr)
        else:
            if initDate.hour == 0:
                daySteps = 0 # Resets day steps
            if initDate.hour == 12:
                daySteps += 500
            if initDate.hour == 18 and initDate.day != 19:
                daySteps += 1000
            if initDate.hour >= 8 and initDate.hour <= 22:
                daySteps += normal(20,10)
            healthInfo.updateHealthInformation('stepCount', elderlyUserId, daySteps, timestr)
        
        ''' UPDATE DATE AND PROGRESS BAR'''
        initDate = initDate + timedelta(hours=1)
        if initDate.day != day:
            day += 1
            bar.next()
    print()
    print("HEALTH DATA COMPLETE")

    return {
        'caregiverUserId': caregiverUserId,
        'elderlyUserId': elderlyUserId
    }

if __name__ == '__main__':
    print(generateAnomaly())
