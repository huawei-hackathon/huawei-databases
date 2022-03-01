from flask import Flask

import food
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/testing")
def testing():
    return "<p>Hello, World!</p>"

app.add_url_rule('/uploadFoodImage', view_func=food.uploadFoodImage, methods=['POST'])

app.run(debug=True, port=80, host="0.0.0.0")

