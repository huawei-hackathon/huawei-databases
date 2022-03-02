import json
import hctools
import base64
from PIL import Image
from io import BytesIO
from flask import request

def uploadFoodImage():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = obj['userId']
    image = obj['image']
    image = Image.open(BytesIO(base64.b64decode(image)))
    image.save('tmp.png', 'png')
    hctools.uploadFoodObject('tmp.png', userId)
    return json.dumps("200")

def queryFoodImages():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = obj['userId']
    date = obj['date']
    return json.dumps(hctools.getFoodObjectsByDate(userId, date))

def queryLastMeal():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = obj['userId']
    return json.dumps(hctools.getLastMeal(userId))
