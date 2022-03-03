import base64
import bcrypt
import mysql.connector 
from password import SQL_PASSWORD

mydb = mysql.connector.connect(
  host="192.168.0.27",
  user="root",
  password=SQL_PASSWORD,
  database='users'
)

mycursor = mydb.cursor()

def createElderly(name, age, caregiverName):
    pass

def createCaregiver(name, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed = hashed.decode('utf-8') 
    # Put hashed as string into database
    sqlCommand = f"INSERT INTO `caregivers` (name, password) VALUES ('{name}', '{hashed}')"
    mycursor.execute(sqlCommand)
    mycursor.execute("SELECT LAST_INSERT_ID()")
    caregiverUserId = mycursor.fetchone()[0]
    return caregiverUserId

def authenticateCaregiver(caregiverUserId, password):
    sqlCommand = f"\
        SELECT * FROM `caregivers` WHERE caregiverUserId = {caregiverUserId} \
    "
    mycursor.execute(sqlCommand)
    hashed = mycursor.fetchone()[2]
    hashed = hashed.encode('utf-8')
    result = bcrypt.checkpw(password.encode('utf-8'), hashed)
    return result

def getElderlyProfile(userId):
    pasr

if __name__ == '__main__':
    id = createCaregiver('daren', 'testing')
    print(authenticateCaregiver(id, 'test'))
    print(authenticateCaregiver(id, 'testing'))
    #mycursor.execute("SELECT * FROM `caregivers`")
    #print(mydb)


