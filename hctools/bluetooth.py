import base64
import mysql.connector 
from pprint import pprint
from password import SQL_PASSWORD
from datetime import datetime, timedelta, date 

def locationUpdate(userId, roomName):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='triggers'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"INSERT INTO `roomentrylog` (userId, roomName, timestamp) VALUES ({userId}, '{roomName}', CURRENT_TIMESTAMP)"
    mycursor.execute(sqlCommand)
    mydb.commit()
    return {'status': 200}

def currentLocation(userId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='triggers'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"SELECT * FROM `roomentrylog` WHERE userId = {userId} ORDER BY timestamp DESC LIMIT 1"
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()
    timeEnterRoom = result[1]
    roomName = result[2]

    now = datetime.now()
    timediff = now - timeEnterRoom

    return {'roomName':roomName, 'timespent': int(timediff.seconds/60)}

def getBluetoothInformation(userId, firstDate, lastDate, frequency):

    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='triggers'
    )

    mycursor = mydb.cursor()
    
    firstDateString = firstDate.strftime("%Y-%m-%d, %H:%M:%S")
    lastDateString = lastDate.strftime("%Y-%m-%d, %H:%M:%S")
    sqlCommand = f"SELECT roomName,timestamp FROM `roomentrylog` WHERE timestamp BETWEEN '{firstDateString}' AND '{lastDateString}' AND userId = {userId}"
    mycursor.execute(sqlCommand)
    result = mycursor.fetchall() 
    pprint(result)
    data = {}
    
    maxValue = 0
    if frequency == 'day': maxValue = 24
    elif frequency == 'week': maxValue = 7
    elif frequency == 'month': maxValue = number_of_days_in_month(lastDate.year, lastDate.month)
    else: maxValue = 12
    if frequency in ['day', 'week']:
        ''' 0 to 23 hours '''
        ''' 0 to 6 days of week '''
        for i in range(maxValue): data[i] = []
    else:
        ''' 1 to 31 days of month '''
        ''' 1 to 12 months of year '''
        for i in range(1, maxValue+1): data[i] = []
	
    for i in result:
        roomName = i[0]
        timestamp = i[1]
        target = i[1].day
        data[target].append({'roomName': roomName, 'timestamp': timestamp})

    for i in data:
        data[i].sort(key = lambda x:x['timestamp'])

    def durationToMidnight(dateObj):
        tix = datetime.date(dateObj.year, dateObj.month, dateObj.day)
        timedelta = dateObj-tix
        return timedelta.seconds

    for date in data:
        if len(data[date]) > 0:
            data[date][0]['duration'] = durationToMidnight(data[date][0]['timestamp'])

    pprint(data[6])

    return {"status":200}
