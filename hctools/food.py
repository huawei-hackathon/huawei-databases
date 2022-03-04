import base64
import subprocess
from uuid import uuid4
from pprint import pprint
from datetime import datetime, timedelta

""" FIXED NAMES OF BUCKETS OR DATABSES """
FOOD_IMAGES_BUCKET = 'hackathon-food-images'

""" PREFIXES IS FOR RUNNING OF HUAWEI LIBRARY COMMANDS """
OBSUTIL_PREFIX = './../obsutil/obsutil'

def uploadFoodObject(imagePath, userId): # Uploads a specific food item
    time = datetime.now().strftime("%Y-%m-%d/%X")
    cmd = f'{OBSUTIL_PREFIX} cp {imagePath} obs://{FOOD_IMAGES_BUCKET}/{userId}/{time}.jpeg'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    return process

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

    print(targets)

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
