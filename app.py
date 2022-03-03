from flask import Flask

from routes import food, users, announcements
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/testing")
def testing():
    return "<p>Hello, World!</p>"

''' FOOD '''
app.add_url_rule('/food/upload', view_func=food.uploadFoodImage, methods=['POST'])
app.add_url_rule('/food/date', view_func=food.queryFoodImages, methods=['GET'])
app.add_url_rule('/food/lastMeal', view_func=food.queryLastMeal, methods=['GET'])

''' USERS ''' 
app.add_url_rule('/users/getProfile', view_func = users.getProfile, methods=['GET'])
app.add_url_rule('/users/createElderly', view_func = users.createElderly, methods=['POST'])
app.add_url_rule('/users/createCaregiver', view_func = users.createCaregiver, methods=['POST'])
app.add_url_rule('/users/authenticateCaregiver', view_func = users.authenticateCaregiver, methods=['POST'])

''' ANNOUNCEMENTS ''' 
app.add_url_rule('/announcementEndpointUpdate', view_func = announcements.announcementEndpointUpdate, methods=['POST'])
app.add_url_rule('/announceMessage', view_func = announcements.announceMessage, methods=['POST'])

app.run(debug=True, port=80, host="0.0.0.0")

