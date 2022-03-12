import json
import base64
import subprocess
from PIL import Image
from io import BytesIO
from uuid import uuid4
from flask import request
from hctools import food

def uploadFoodImage():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    image = obj['image']
    image = Image.open(BytesIO(base64.b64decode(image)))
    imagePath = f'tmp/{uuid4()}.jpg'
    image.save(imagePath, 'png')
    food.uploadFoodObject(imagePath, userId)
    #subprocess.run(f"rm {imagePath}", shell=True)
    return json.dumps({'status':200})

def queryFoodImages():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    date = obj['date']
    return json.dumps(food.getFoodObjectsByDate(userId, date))

def queryLastMeal():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    return json.dumps(food.getLastMeal(userId))
