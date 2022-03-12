import base64
import subprocess
import mysql.connector 
from uuid import uuid4
from pprint import pprint
from password import SQL_PASSWORD
from datetime import datetime, timedelta
from foodAI import getFoodGroups

""" FIXED NAMES OF BUCKETS OR DATABSES """
FOOD_IMAGES_BUCKET = 'hackathon-food-images'

""" PREFIXES IS FOR RUNNING OF HUAWEI LIBRARY COMMANDS """
OBSUTIL_PREFIX = './../obsutil/obsutil'

def uploadFoodObject(imagePath, userId): # Uploads a specific food item
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='food'
    )

    mycursor = mydb.cursor()
    
    ''' UPLOAD IMAGINE TO OBS ''' 
    imgUUID = uuid4()
    cmd = f'{OBSUTIL_PREFIX} cp {imagePath} obs://{FOOD_IMAGES_BUCKET}/{imgUUID}.jpg'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    imgLink = f"https://{FOOD_IMAGES_BUCKET}.obs.ap-southeast-3.myhuaweicloud.com/{imgUUID}.jpg"

    sqlCommand = f"INSERT INTO `meals` (userId, timestamp, imgLink) VALUES ({userId}, CURRENT_TIMESTAMP, '{imgLink}')"
    mycursor.execute(sqlCommand)
    mydb.commit()

    mycursor.execute("SELECT LAST_INSERT_ID()")
    imgId = mycursor.fetchone()[0]

    foodGroups = getFoodGroups(imagePath)
    for food in foodGroups:
        sqlCommand = f"INSERT INTO `foodgroups` (imgId, foodType, foodGroup, confidence) VALUES ({imgId}, '{food['foodType']}', '{food['foodGroup']}', {food['confidence']})"
        mycursor.execute(sqlCommand)
        mydb.commit()

    return 0

def getFoodObjectsByDate(userId, date): # Gets all images from a certain date
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='food'
    )

    mycursor = mydb.cursor()
    startTime = datetime(date.year, date.month, date.day, 0,0,0)
    endTime = datetime(date.year, date.month, date.day, 23, 59, 59)
    
    sqlCommand = f"SELECT * FROM `meals` WHERE userId = {userId} AND timestamp BETWEEN '{startTime}' AND '{endTime}' ORDER BY timestamp DESC"
    mycursor.execute(sqlCommand)
    results = mycursor.fetchall()

    return [{
        'mealId': result[0],
        'userId': result[1],
        'timestamp': result[2].strftime("%Y-%M-%d %X"),
        'imgUrl': result[3]
    } for result in results]

def getLastMeal(userId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='food'
    )

    mycursor = mydb.cursor()
    
    sqlCommand = f'SELECT * FROM `meals` WHERE userId = {userId} ORDER BY timestamp DESC'
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()

    return {
        'mealId': result[0],
        'userId': result[1],
        'timestamp': result[2].strftime("%Y-%M-%d %X"),
        'imgUrl': result[3]
    }

def updateFoodGroup(foodId, foodGroup):
    sqlCommand = f"UPDATE `foodgroups` SET foodGroup = '{foodGroup}' WHERE foodId = {foodId}"
    mycursor.execute(sqlCommand)
    mydb.commit()
    return {'status':200}

if __name__ == '__main__':

    pass
