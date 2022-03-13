import json
from uuid import uuid4
from flask import request, render_template
from hctools import reports
from datetime import datetime
from mockdata import mockReport, mockAnomaly

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
        return render_template('report-not-found.html', error = 'No Report Found')

    now = datetime.now()
    timestamp = reportInfo['timestamp']
    userId = reportInfo['userId']
    difference = now - timestamp
    timeSeconds = difference.total_seconds()
    if timeSeconds > 3600:
        return render_template('report-not-found.html', error = 'Report Expired')

    data = reports.getData(userId)

    return render_template('index.html', data=data)

def getMockReport():
    return json.dumps(mockReport.generateReport())

def getMockAnomaly():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    heartRate = int(obj['heartRate'])
    sleepSeconds = int(obj['sleepSeconds'])
    stepAsymmetry = int(obj['stepAsymmetry'])
    stepCount = int(obj['stepCount'])

    return json.dumps(mockAnomaly.generateAnomaly(heartRate, sleepSeconds, stepAsymmetry, stepCount))
