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

def recordedMessage(userId, audio):
    pass

def announceMessage(userId, announcementText):
    ''' INSERT INTO DB '''
    sqlCommand = f"INSERT INTO `announcements` (userId, announcementText) VALUES ({userId}, '{announcementText}')"
    mycursor.execute(sqlCommand)
    mydb.commit()

    ''' SENDING REQUEST ''' 
    sqlCommand = f"SELECT tunnelUrl FROM `tunnels` WHERE userId = '{userId}'"
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()[0]
    if result == None:
        return {'status': 300, 'error': 'No tunnel URL found!'}
    try:
        url = f'{result}/announceMessage'
        data = {'text': announcementText}
        response = requests.post(url, json=data)
        return {'status': response.status_code}
    except:
        return {'status': 300, 'error': 'Announcement Failed!'}
    return {}
    pass

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

