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
from hctools import announcements, food, healthInfo, users

def mean(array):
    return round(sum(array) / len(array), 2)

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

def sleepTimeHelp(sleepSeconds):
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
    lastday = date(now.year, now.month+1, 1) - timedelta(days=1) # TODO:CHANGE IN CASE IT CROSSES A YEAR BOUNDARY
    firstday = lastday - relativedelta(months=1)
    daysInMonth = number_of_days_in_month(lastday.year, lastday.month)

    ''' POPULATING DATA '''
    elderlyInfo = users.getElderlyProfile(userId)

    heartRates = healthInfo.getHealthInformation("heartRate", userId, firstday, lastday, "month")
    heartRateList = [0] * daysInMonth
    for i in heartRates: heartRateList[i['x']-1] = i['y']

    steps = healthInfo.getHealthInformation("stepCount", userId, firstday, lastday, "month")
    stepsList = [0] * daysInMonth
    for i in steps: stepsList[i['x']-1] = i['y']

    sleepTimes = healthInfo.getHealthInformation("sleepSeconds", userId, firstday, lastday, "month")
    sleepTimeList = [0] * daysInMonth
    for i in sleepTimes: sleepTimeList[i['x']-1] = i['y']

    asymmetry = healthInfo.getHealthInformation("stepAsymmetry", userId, firstday, lastday, "month")
    asymmetryList = [0] * daysInMonth
    for i in asymmetry: asymmetryList[i['x']-1] = i['y']

    data = {
            "elderlyName": elderlyInfo['name'],
            "elderlyAge": elderlyInfo['age'],
            "anomalyDetectionText": "John Doe is feeling very sad. He is not feeling well. He seems to be spending many hours in the toilet compared to previous month. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", # this one just leave something default now since we dont have the model yet
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
                "data": [8.6, 7.0, 11.3, 8.1, 8.4, 9.4, 8.1, 8.8, 8.5, 8.2, 7.4, 8.9, 8.3, 7.8, 8.4, 6.8, 8.7, 6.6, 9.0, 7.3, 5.0, 9.7, 5.1, 4.6, 8.2, 7.9, 4.4, 7.4, 8.3, 6.7, 8.0]
                }, {
                "label": "Bedroom",
                "backgroundColor": "#e74a3b",
                "hoverBackgroundColor": "#A8362C",
                "data": [6.6, 6.9, 6.8, 7.9, 6.5, 6.4, 6.2, 6.3, 6.5, 7.3, 6.6, 7.8, 7.3, 7.3, 7.2, 7.1, 6.5, 7.9, 6.4, 6.7, 7.5, 6.8, 7.8, 7.7, 6.0, 7.4, 7.4, 6.0, 7.3, 6.7, 7.7]
                }, {
                "label": "Bathroom",
                "backgroundColor": "#36b9cc",
                "hoverBackgroundColor": "#247E8C",
                "data": [0.7, 1.7, 0.5, 0.8, 0.5, 1.0, 1.1, 0.8, 0.6, 1.4, 1.0, 1.4, 0.6, 1.0, 1.8, 0.8, 0.7, 1.9, 1.8, 1.7, 1.9, 1.5, 1.9, 1.9, 0.6, 2.0, 1.7, 1.9, 0.5, 1.7, 1.5]
                }, {
                "label": "Kitchen",
                "backgroundColor": "#1cc88a",
                "hoverBackgroundColor": "#13875D",
                "data": [3.4, 3.0, 3.3, 3.8, 3.0, 3.6, 4.1, 4.1, 4.0, 3.3, 3.8, 3.4, 3.6, 4.3, 3.3, 3.3, 3.3, 3.9, 3.9, 3.3, 4.3, 3.4, 3.6, 4.1, 3.5, 3.1, 4.5, 3.8, 3.1, 3.4, 4.3]
                }, {
                "label": "Outside",
                "backgroundColor": "#C0CCC9",
                "hoverBackgroundColor": "#88908E",
                "data": [4.7, 5.4, 2.1, 3.4, 5.6, 3.6, 4.5, 4.0, 4.4, 3.8, 5.2, 2.5, 4.2, 3.6, 3.3, 6.0, 4.8, 3.7, 2.9, 5.0, 5.3, 2.6, 5.6, 5.7, 5.7, 3.6, 6.0, 4.9, 4.8, 5.5, 2.5]
                }
            ],

            "avgSteps": mean(stepsList),
            "avgHeartRate": mean(heartRateList),
            "avgSleepTime": sleepTimeHelp(mean(sleepTimeList)),
            "avgWalkingAsymmetry": mean(asymmetryList),

            "dietLabels": ["Carbohydrates", "Vegetable", "Protein", "idk"],
            "dietData": [60, 20, 40, 10],

            "bluetoothPieChartLabels": ["Living Room", "Bedroom", "Bathroom", "Kitchen", "Outside"],
            "bluetoothPieChartData": [55, 70, 15, 20, 50],

            "dietAnalysis": "Idk some body of text here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", # we dont have the actual data yet
    }

    return data

if __name__ == '__main__':
    pprint(getData(21))
