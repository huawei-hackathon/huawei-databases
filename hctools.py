""" 
HCTOOLS.py
HUAWEI CLOUD TOOLS
"""
import subprocess
from pprint import pprint
from datetime import datetime, timedelta

""" PREFIXES IS FOR RUNNING OF HUAWEI LIBRARY COMMANDS """
OBSUTIL_PREFIX = './../obsutil/obsutil'

def uploadFoodObject(imagePath, userId):
    time = (datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d/%X")
    cmd = f'{OBSUTIL_PREFIX} cp {imagePath} obs://spark-food-images/{userId}/{time}.jpeg'
    process = subprocess.run(cmd, shell=True, capture_output=True)
    pprint(process)
    return process

if __name__ == '__main__':
    uploadFoodObject('app.py', 'darentrw') 
    pass
