import base64
import requests
import mysql.connector 
from password import SQL_PASSWORD

mydb = mysql.connector.connect(
  host="192.168.0.27",
  user="root",
  password=SQL_PASSWORD,
  database='communication'
)

mycursor = mydb.cursor()

""" FIXED NAMES OF BUCKETS OR DATABSES """
FOOD_IMAGES_BUCKET = 'hackathon-food-images'

""" PREFIXES IS FOR RUNNING OF HUAWEI LIBRARY COMMANDS """
OBSUTIL_PREFIX = './../obsutil/obsutil'

def sendRequest(command, userId, announcementText):
    sqlCommand = f"SELECT tunnelUrl FROM `tunnels` WHERE userId = '{userId}'"
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()[0]
    if result == None:
        return {'status': 300, 'error': 'No tunnel URL found!'}
    url = f'{result}/{command}' # Either recorded or announce message
    data = {'text': announcementText}
    try:
        response = requests.post(url, json=data)
        return {'status': response.status_code}
    except:
        return {'status': 300, 'error': 'Announcement Failed!'}
    return {}

def recordedMessage(userId, audio):
    ''' INSERT INTO DB '''
    sqlCommand = f"INSERT INTO `announcements` (userId) VALUES ({userId})"
    mycursor.execute(sqlCommand)
    mydb.commit()
    mycursor.execute("SELECT LAST_INSERT_ID()")
    announcementId = mycursor.fetchone()[0]

    sqlCommand
    ''' INSERT INTO OBS'''
    with open("tmp.mp3", "rb") as audioFile:
        audioFile.write(base64.b64decode(audioFile))

    cmd = f'{OBSUTIL_PREFIX} cp {imagePath} obs://{FOOD_IMAGES_BUCKET}/{userId}/{time}.jpeg'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    return process

    return sendRequest('recordedMessage', userId, '')
    pass

def announceMessage(userId, announcementText):
    ''' INSERT INTO DB '''
    sqlCommand = f"INSERT INTO `announcements` (userId, announcementText) VALUES ({userId}, '{announcementText}')"
    mycursor.execute(sqlCommand)
    mydb.commit()

    ''' SENDING REQUEST ''' 
    return sendRequest('announceMessage', userId, announcementText)

def announcementEndpointUpdate(userId, tunnelUrl):
    ''' CHECK IF USERID IS ALREADY IN DB ''' 
    sqlCommand = f"SELECT userId FROM `tunnels` WHERE userId = {userId}"
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()
    
    ''' NOT YET IN DB '''
    if result == None:
        mycursor.execute (f"INSERT INTO `tunnels` (userId, tunnelUrl) VALUES ({userId}, '{tunnelUrl}')")
        mydb.commit()
        return {'status': 200, 'comments': 'Created New Entry'}
    else:
        mycursor.execute (f"UPDATE `tunnels` SET tunnelUrl = '{tunnelUrl}' WHERE userId = {userId}")
        mydb.commit()
        return {'status': 200, 'comments': 'Updated Existing Entry'}

if __name__ == '__main__':
    announcementEndpointUpdate(11, 'https://tidy-insect-49.loca.lt/') 
    announceMessage(11, 'hello!')

    recordedMessage(11, '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')
