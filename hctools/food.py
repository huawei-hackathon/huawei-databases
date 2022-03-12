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
    imgLink = f"https://{FOOD_IMAGES_BUCKET}.obs.ap-southeast-3.myhuaweicloud.com/{imgUUID}.jpeg"

    sqlCommand = f"INSERT INTO `meals` (userId, timestamp, imgLink) VALUES ({userId}, CURRENT_TIMESTAMP, '{imgLink}')"
    mycursor.execute(sqlCommand)
    mydb.commit()

    mycursor.execute("SELECT LAST_INSERT_ID()")
    imgId = mycursor.fetchone()[0]

    foodGroups = getFoodGroups(imagePath)
    print(foodGroups)
    for food in foodGroups:
        sqlCommand = f"INSERT INTO `foodgroups` (imgId, foodType, foodGroup, confidence) VALUES ({imgId}, '{food['foodType']}', '{food['foodGroup']}', {food['confidence']}"
        mycursor.execute(sqlCommand)
        mydb.commit()

    return 0

def getFoodObjectsByDate(userId, date): # Gets all images from a certain date
    cmd = f'{OBSUTIL_PREFIX} ls obs://{FOOD_IMAGES_BUCKET}/{userId}/{date}/ -s'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = process.stdout.decode("utf-8")
    byLineOutput = stdout.split("\n")
    if 'Object list:' not in byLineOutput: # No objects found
        return []
    startInd = byLineOutput.index('Object list:') + 1
    targets = [] # Target downloads
    while startInd < len(byLineOutput):
        if (byLineOutput[startInd][:3] == 'obs'):
            fileName = byLineOutput[startInd]
            fileNoExt = fileName.split('.')[0]
            time = fileNoExt.split('/')[-1]

            urlSuffix = fileName.split('//')[-1]
            ''' REMOVE BUCKET NAME FROM URL '''
            urlSuffix = '/'.join(urlSuffix.split('/')[1:])
            urlPrefix = f'https://{FOOD_IMAGES_BUCKET}.obs.ap-southeast-3.myhuaweicloud.com/'
            imgUrl = urlPrefix + urlSuffix
            targets.append({
                'imgUrl': imgUrl,
                'time': time
            })
            startInd += 1
        else: 
            break

    return targets

def getLastMeal(userId):
    cmd = f'{OBSUTIL_PREFIX} ls obs://{FOOD_IMAGES_BUCKET}/{userId}/ -s'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = process.stdout.decode("utf-8")
    byLineOutput = stdout.split("\n")
    if 'Folder list:' not in byLineOutput: # No objects found
        return {}
    startInd = byLineOutput.index('Folder list:') + 1
    lastDate = ''
    while startInd < len(byLineOutput):
        if (byLineOutput[startInd][:3] == 'obs'):
            lastDate = byLineOutput[startInd]
            startInd += 1
        else:
            break
    if lastDate == ' ':
        return {}
    cmd = f'{OBSUTIL_PREFIX} ls {lastDate} -s'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = process.stdout.decode("utf-8")
    byLineOutput = stdout.split("\n")
    if 'Object list:' not in byLineOutput: # No objects found
        return {}
    startInd = byLineOutput.index('Object list:') + 1
    fileName = ''
    while startInd < len(byLineOutput):
        if (byLineOutput[startInd][:3] == 'obs'):
            fileName = byLineOutput[startInd]
            startInd += 1
        else:
            break
    urlSuffix = fileName.split('//')[-1]
    ''' REMOVE BUCKET NAME FROM URL '''
    urlSuffix = '/'.join(urlSuffix.split('/')[1:])
    urlPrefix = f'https://{FOOD_IMAGES_BUCKET}.obs.ap-southeast-3.myhuaweicloud.com/'
    fileNoExt = fileName.split('.')[0]
    time = fileNoExt.split('/')[-1]
    date = fileNoExt.split('/')[-2]
    
    result = {
        'time':time,
        'date':date,
        'url':urlPrefix+urlSuffix
    }

    return result

if __name__ == '__main__':
    getLastMeal('testindaren')

    pass
