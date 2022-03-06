import base64
import requests
import subprocess
import mysql.connector 
from uuid import uuid4
from io import BytesIO
from uuid import uuid4
from pprint import pprint
from password import SQL_PASSWORD

mydb = mysql.connector.connect(
  host="192.168.0.27",
  user="root",
  password=SQL_PASSWORD,
  database='reports'
)

mycursor = mydb.cursor()

def generateReport(uuid, userId):
    sqlCommand = f"INSERT INTO `reports` (reportUUID, userId, timestamp) VALUES ('{uuid}', {userId}, CURRENT_TIMESTAMP)"
    mycursor.execute(sqlCommand)
    mydb.commit()

def getReportInfo(uuid):
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

if __name__ == '__main__':
    id = uuid4()
    generateReport(id, 15)
    print(getReportInfo(id))
