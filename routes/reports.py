import json
from uuid import uuid4
from flask import request, render_template
from hctools import reports
from datetime import datetime

def generateReport():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    id = uuid4()
    reports.generateReport(id, userId)
    return {"id": id}

def getReport(reportUUID):
    ''' CHECK IF REPORT UUID IS VALID '''
    reportInfo = reports.getReportInfo(reportUUID)

    if reportInfo == {}:
        return render_template('report-not-found.html', error = 'No report found')

    now = datetime.now()
    timestamp = reportInfo['timestamp']
    userId = reportInfo['userId']
    difference = now - timestamp
    print(difference)

    data = {
            "elderlyName": "John Doe",
            "elderlyAge": "42",
            "anomalyDetectionText": "John Doe is feeling very sad. He is not feeling well. He seems to be spending many hours in the toilet compared to previous month. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", # this one just leave something default now since we dont have the model yet
            "datesOfMonth": [i for i in range(1, 32)],
            "month": "January",
            "year": "2022",

            "heartRateList": [97, 109, 104, 107, 94, 98, 96, 93, 101, 109, 98, 90, 106, 99, 91, 97, 104, 90, 99, 103, 90, 110, 97, 94, 94, 101, 91, 106, 107, 95, 103],
            "stepsList": [6869, 4430, 6471, 3305, 5604, 4196, 4028, 6165, 5460, 3464, 4264, 6391, 7897, 4917, 3962, 5551, 4210, 5009, 6078, 4491, 7890, 3561, 6339, 3470, 6215, 7790, 7030, 7685, 5829, 4742, 4405],
            "sleepTimeList": [9.3, 8.7, 9.1, 8.9, 9.3, 7.5, 8.4, 9.1, 8.5, 9.4, 9.8, 8.5, 8.4, 10.0, 9.8, 8.0, 9.9, 8.3, 8.8, 7.7, 7.7, 8.1, 8.3, 7.9, 7.7, 9.5, 8.1, 7.5, 8.7, 8.5, 9.8],
            "asymmetryList": [7.0, 4.0, 5.0, 4.0, 3.0, 7.0, 8.0, 3.0, 3.0, 5.0, 5.0, 6.0, 7.0, 3.0, 8.0, 5.0, 6.0, 8.0, 5.0, 3.0, 6.0, 5.0, 8.0, 7.0, 3.0, 8.0, 5.0, 3.0, 5.0, 6.0, 3.0],

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

            "avgSteps": "10,001",
            "avgHeartRate": "104",
            "avgSleepTime": ['8', '10'], # [hours, minutes]
            "avgWalkingAsymmetry": "7.9",

            "dietLabels": ["Carbohydrates", "Vegetable", "Protein", "idk"],
            "dietData": [60, 20, 40, 10],

            "bluetoothPieChartLabels": ["Living Room", "Bedroom", "Bathroom", "Kitchen", "Outside"],
            "bluetoothPieChartData": [55, 70, 15, 20, 50],

            "dietAnalysis": "Idk some body of text here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", # we dont have the actual data yet
        }

    return render_template('index.html', data=data)
