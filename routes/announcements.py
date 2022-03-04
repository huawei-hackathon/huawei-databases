import json
from flask import request
from hctools import announcements

def announcementEndpointUpdate():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    tunnelUrl = obj['tunnelUrl']
    return json.dumps(announcements.announcementEndpointUpdate(userId, tunnelUrl))

def announceMessage():
    obj=request.data.decode("utf-8")
    obj = obj.replace("'", '"') # Replace ' with " for json decoding
    obj = json.loads(obj)
    userId = int(obj['userId'])
    text = obj['text']
    return json.dumps(announcements.announceMessage(userId, text))
