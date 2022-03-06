import base64
import bcrypt
import mysql.connector 
from password import SQL_PASSWORD

def createElderly(name, age, caregiverUserId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='users'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"INSERT INTO `elderly` (name, age, caregiverUserId) VALUES ('{name}', {age}, {caregiverUserId})"
    mycursor.execute(sqlCommand)
    mydb.commit()
    mycursor.execute("SELECT LAST_INSERT_ID()")
    userId = mycursor.fetchone()[0]
    return {'userId': userId}

def createCaregiver(name, password):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='users'
    )

    mycursor = mydb.cursor()

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed = hashed.decode('utf-8') 
    # Put hashed as string into database
    sqlCommand = f"INSERT INTO `caregivers` (name, password) VALUES ('{name}', '{hashed}')"
    mycursor.execute(sqlCommand)
    mydb.commit()
    mycursor.execute("SELECT LAST_INSERT_ID()")
    caregiverUserId = mycursor.fetchone()[0]
    return {'caregiverUserId': caregiverUserId}

def authenticateCaregiver(caregiverUserId, password):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='users'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"\
        SELECT * FROM `caregivers` WHERE caregiverUserId = {caregiverUserId} \
    "
    print(sqlCommand)
    mycursor.execute(sqlCommand)
    hashed = mycursor.fetchone()[2]
    hashed = hashed.encode('utf-8')
    result = bcrypt.checkpw(password.encode('utf-8'), hashed)
    return {'status': result}

def getElderlyProfile(userId):
    mydb = mysql.connector.connect(
        host="192.168.0.27",
        user="root",
        password=SQL_PASSWORD,
        database='users'
    )

    mycursor = mydb.cursor()

    sqlCommand = f"\
        SELECT * FROM `elderly` WHERE userId = {userId} \
    "
    mycursor.execute(sqlCommand)
    result = mycursor.fetchone()
    if result == None:
        return {}
    else:
        return {
            'userId': result[0],
            'name': result[1],
            'age': result[2],
            'caregiverUserId': result[3]
        }

if __name__ == '__main__':
    id = createCaregiver('daren', 'testing')['caregiverUserId']
    print(authenticateCaregiver(id, 'test'))
    print(authenticateCaregiver(id, 'testing'))
    userId = createElderly('glenda', 18, id)['userId']
    print(getElderlyProfile(userId))
    #mycursor.execute("SELECT * FROM `caregivers`")
    #print(mydb)


