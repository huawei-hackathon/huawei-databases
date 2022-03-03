import json
from flask import request
from hctools import users

def getProfile():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    return json.dumps(users.getElderlyProfile(userId))

def createElderly():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    name = obj['name']
    age = int(obj['age'])
    caregiverUserId = int(obj['caregiverUserId'])
    return json.dumps(users.createElderly(name, age, caregiverUserId))

def createCaregiver():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    name = obj['name']
    password = obj['password']
    return json.dumps(users.createCaregiver(name, password))

def authenticateCaregiver():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    caregiverUserId = int(obj['caregiverUserId'])
    password = obj['password']
    return json.dumps(users.authenticateCaregiver(caregiverUserId, password))
