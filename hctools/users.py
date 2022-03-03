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
    pass

def getElderlyProfile(name):
    pass

if __name__ == '__main__':
    print(mydb)


