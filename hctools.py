""" 
HCTOOLS.py
HUAWEI CLOUD TOOLS
"""
import base64
import subprocess
from uuid import uuid4
from pprint import pprint
from datetime import datetime, timedelta

""" PREFIXES IS FOR RUNNING OF HUAWEI LIBRARY COMMANDS """
OBSUTIL_PREFIX = './../obsutil/obsutil'

def uploadFoodObject(imagePath, userId): # Uploads a specific food item
    time = datetime.now().strftime("%Y-%m-%d/%X")
    cmd = f'{OBSUTIL_PREFIX} cp {imagePath} obs://spark-food-images/{userId}/{time}.jpeg'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    return process

def getFoodObjectsByDate(userId, date): # Gets all images from a certain date
    cmd = f'{OBSUTIL_PREFIX} ls obs://spark-food-images/{userId}/{date}/ -s'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = process.stdout.decode("utf-8")
    byLineOutput = stdout.split("\n")
    startInd = byLineOutput.index('Object list:') + 1
    targets = {} # Target downloads
    while startInd < len(byLineOutput):
        if (byLineOutput[startInd][:3] == 'obs'):
            targets[byLineOutput[startInd]] = ''
            startInd += 1
        else: 
            break

    tmpDir = uuid4()
    subprocess.run(f'mkdir {tmpDir}', shell=True)
    for target in targets.keys():
        tmpId = uuid4()
        cmd = f'{OBSUTIL_PREFIX} cp {target} {tmpDir}/{tmpId}.png'
        process = subprocess.run(cmd, shell=True, capture_output=True)
        with open(f'{tmpDir}/{tmpId}.png', "rb") as imageString:
            convertedString = base64.b64encode(imageString.read())
            targets[target] = convertedString.decode()
    subprocess.run(f'rm -rf {tmpDir}', shell=True)
    return targets

if __name__ == '__main__':
    getFoodObjectsByDate('darentan', '2022-03-01')

    pass
