import base64
import requests
import subprocess
import mysql.connector 
from uuid import uuid4
from pprint import pprint
from calendar import monthrange
from password import SQL_PASSWORD
from datetime import datetime, timedelta, date 
from dateutil.relativedelta import relativedelta
from hctools import announcements, food, healthInfo, users, bluetooth

def mean(array):
    return round(sum(array) / len(array), 1)

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

def sleepTimeHelp(sleepSeconds):
    sleepSeconds *= 3600
    sleepMinutes = round(sleepSeconds/60)
    sleepHours = int(sleepMinutes/60)
    sleepMinutes -= 60*sleepHours
    return [sleepHours, sleepMinutes]

def generateReport(uuid, userId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='reports'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"INSERT INTO `reports` (reportUUID, userId, timestamp) VALUES ('{uuid}', {userId}, CURRENT_TIMESTAMP)"
    mycursor.execute(sqlCommand)
    mydb.commit()

def getReportInfo(uuid):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='reports'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"SELECT userId, timestamp FROM `reports` WHERE reportUUID = '{uuid}'"
    mycursor.execute(sqlCommand)
    value = mycursor.fetchone()
    if value == None:
        return {}
    else:
        return {
            'userId': value[0],
            'timestamp': value[1]
        }

def getData (userId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='reports'
    )

    mycursor = mydb.cursor()
    
    ''' GENERAL DATE INFORMATION ''' 
    now = datetime.now()
    ''' LAST DAY IS LAST DAY LAST SECOND OF OUR MONTH '''
    lastday = datetime(now.year, now.month+1, 1) - timedelta(seconds=1) # TODO:CHANGE IN CASE IT CROSSES A YEAR BOUNDARY
    firstday = lastday - relativedelta(months=1)
    daysInMonth = number_of_days_in_month(lastday.year, lastday.month)

    ''' POPULATING DATA '''
    elderlyInfo = users.getElderlyProfile(userId)
    name = elderlyInfo['name']

    ''' HEART RATES ''' 

    heartRates = healthInfo.getHealthInformation("heartRate", userId, firstday, lastday, "month")
    heartRateList = [0] * daysInMonth
    for i in heartRates: heartRateList[i['x']-1] = i['y']

    ''' STEP COUNT ''' 

    steps = healthInfo.getHealthInformation("stepCount", userId, firstday, lastday, "month")
    stepsList = [0] * daysInMonth
    for i in steps: stepsList[i['x']-1] = i['y']
    
    ''' SLEEP TIMES ''' 

    sleepTimes = healthInfo.getHealthInformation("sleepSeconds", userId, firstday, lastday, "month")
    sleepTimeList = [0] * daysInMonth
    for i in sleepTimes: sleepTimeList[i['x']-1] = i['y']
    for i in range(len(sleepTimeList)): 
        sleepTimeList[i] = round(sleepTimeList[i]/3600, 2)

    ''' STEP ASYMMETRY ''' 

    asymmetry = healthInfo.getHealthInformation("stepAsymmetry", userId, firstday, lastday, "month")
    asymmetryList = [0] * daysInMonth
    for i in asymmetry: asymmetryList[i['x']-1] = i['y']

    ''' BLUETOOTH INFORMATION '''

    roomNames = ["Living Room", "Bedroom", "Bathroom", "Kitchen", "Outside"]
    bluetoothInfoResult = bluetooth.getBluetoothInformation(userId, firstday, lastday, "month")
    bluetoothInfo = {}
    for i in bluetoothInfoResult:
        bluetoothInfo[i['roomName']] = [round(x/60, 2) for x in i['times']]
    outingDays = len([i for i in bluetoothInfo['Outside'] if i > 1e-7]) # NUMBER OF DAYS TIME SPENT OUTSIDE IS NONZERO 

    pieData = []
    for i in roomNames:
        pieData.append(sum(bluetoothInfo[i]))
        pieData[-1] = round(pieData[-1], 0)
    percentages = [round(i/sum(pieData), 1) for i in pieData]
    pieDataWithText = [f"{pieData[i]} ({percentages[i]}%)" for i in range(len(pieData))]
    
    ''' DISPLAY TEXT ''' 
    displayText = ""

    ''' SENTIMENT ANLYSIS ''' 
    sentimentText = ""
    result = announcements.analyseConversation(userId, firstday, lastday)
    elderlyMessages = result['elderlyMessages']
    caregiverMessages = result['caregiverMessages']
    meanSentiment = result['meanSentiment']

    if meanSentiment < 0.5:
        if mean(stepsList) <= 1000 or outingDays < 15:
            sentimentText += f"{name} has been staying at home for longer periods of time, merely going out {outingDays} a month and registering a low step count. " 
        if elderlyMessages >= 2* caregiverMessages:
            sentimentText += f"{name} seems to have a one-sided interaction with his caregiver: while {name} has sent {elderlyMessages} to his caregiver, his caregiver has only replied with {caregiverMessages} messages. "
            sentimentText += f"His messages often contain an annoyed undertone with a mean sentiment value of {meanSentiment}, which could possibly indicate feelings of loneliness."
        elif elderlyMessages <= 30 or elderlyMessages *2 <= caregiverMessages:
            sentimentText += f"{name} seems to be an introvert. While his caregiver has sent him {caregiverMessages}, he has only chosen to respond {elderlyMessages} times. His messages have amean sentiment value of {meanSentiment}, a possible sign that he rather be left to himself for greater periods of time. "
    else:
        if outingDays >= 15:
            sentimentText += f"{name} has been going out often, leaving his home a grand total of {outingDays} times. "
        if elderlyMessages >= 2* caregiverMessages:
            sentimentText += f"{name} enjoys frequently contacting his caregiver, sending him {elderlyMessages} messages over the course of the month. His messages are often joyus with a mean sentiment value of {meanSentiment}, implying that he is in a good mood! "
        else:
            sentimentText += f"{name} enjoys a healthy relationship with his caregiver, in total exchanging {caregiverMessages + elderlyMessages} messages over the course of month. His messages are often joyus with a mean sentiment value of {meanSentiment}, implying that he is in a good mood! "
            
    displayText += sentimentText

    data = {
            "elderlyName": elderlyInfo['name'],
            "elderlyAge": elderlyInfo['age'],
            "anomalyDetectionText": displayText,
            "datesOfMonth": [i for i in range(1, daysInMonth+1)],
            "month": lastday.strftime("%B"),
            "year": lastday.year,
            "heartRateList": heartRateList,
            "stepsList": stepsList,
            "sleepTimeList": sleepTimeList,
            "asymmetryList": asymmetryList,

            "bluetoothGraphDatasets": [{
                "label": "Living Room",
                "backgroundColor": "#4e73df",
                "hoverBackgroundColor": "#2e59d9",
                "data": bluetoothInfo['Living Room']
                }, {
                "label": "Bedroom",
                "backgroundColor": "#1cc88a",
                "hoverBackgroundColor": "#13875D",
                "data": bluetoothInfo['Bedroom']
                }, {
                "label": "Bathroom",
                "backgroundColor": "#36b9cc",
                "hoverBackgroundColor": "#247E8C",
                "data": bluetoothInfo['Bathroom']
                }, {
                "label": "Kitchen",
                "backgroundColor": "#e74a3b",
                "hoverBackgroundColor": "#A8362C",
                "data": bluetoothInfo['Kitchen']
                }, {
                "label": "Outside",
                "backgroundColor": "#C0CCC9",
                "hoverBackgroundColor": "#88908E",
                "data": bluetoothInfo['Outside']
                }
            ],

            "avgSteps": mean(stepsList),
            "avgHeartRate": mean(heartRateList),
            "avgSleepTime": sleepTimeHelp(mean(sleepTimeList)),
            "avgWalkingAsymmetry": mean(asymmetryList),

            "dietLabels": ["Carbohydrates", "Vegetable", "Protein", "idk"],
            "dietData": [60, 20, 40, 10],

            "bluetoothPieChartLabels": roomNames,
            "bluetoothPieChartData": pieData,

            "dietAnalysis": "Idk some body of text here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", # we dont have the actual data yet
    }

    return data

if __name__ == '__main__':
    pprint(getData(21))
