from flask import Flask, render_template

from routes import food, users, announcements, healthInfo, reports, bluetooth
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

''' FOOD '''
app.add_url_rule('/food/upload', view_func=food.uploadFoodImage, methods=['POST'])
app.add_url_rule('/food/date', view_func=food.queryFoodImages, methods=['POST'])
app.add_url_rule('/food/lastMeal', view_func=food.queryLastMeal, methods=['POST'])

''' USERS ''' 
app.add_url_rule('/users/getElderlyProfile', view_func = users.getElderlyProfile, methods=['POST'])
app.add_url_rule('/users/getCaregiverProfile', view_func = users.getCaregiverProfile, methods=['POST'])
app.add_url_rule('/users/createElderly', view_func = users.createElderly, methods=['POST'])
app.add_url_rule('/users/createCaregiver', view_func = users.createCaregiver, methods=['POST'])
app.add_url_rule('/users/authenticateCaregiver', view_func = users.authenticateCaregiver, methods=['POST'])

''' ANNOUNCEMENTS ''' 
app.add_url_rule('/announcementEndpointUpdate', view_func = announcements.announcementEndpointUpdate, methods=['POST'])
app.add_url_rule('/announceMessage', view_func = announcements.announceMessage, methods=['POST'])
app.add_url_rule('/recordedCaregiverMessage', view_func = announcements.recordedCaregiverMessage, methods=['POST'])
app.add_url_rule('/recordedElderlyMessage', view_func = announcements.recordedElderlyMessage, methods=['POST'])
app.add_url_rule('/getConversation', view_func = announcements.getConversation, methods=['POST'])

''' HEALTH INFORMATION '''
app.add_url_rule('/<healthInfoType>/<frequency>', view_func = healthInfo.getHealthInformation, methods=['POST'])
app.add_url_rule('/<healthInfoType>/postData', view_func = healthInfo.updateHealthInformation, methods=['POST'])

''' REPORTS '''
app.add_url_rule('/generateReport', view_func = reports.generateReport, methods = ['POST'])
app.add_url_rule('/getReport/<reportUUID>', view_func = reports.getReport, methods = ['GET'])

''' BLUETOOTH '''
app.add_url_rule('/locationUpdate', view_func = bluetooth.locationUpdate, methods=['POST'])
app.add_url_rule('/currentLocation', view_func = bluetooth.currentLocation, methods=['POST'])
app.add_url_rule('/bluetooth/<frequency>', view_func = bluetooth.getBluetoothInformation, methods=['POST'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(debug=True, port=80, host="0.0.0.0")
