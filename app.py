from flask import Flask

import food
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/testing")
def testing():
    return "<p>Hello, World!</p>"

app.add_url_rule('/food/upload', view_func=food.uploadFoodImage, methods=['POST'])
app.add_url_rule('/food/date', view_func=food.queryFoodImages, methods=['GET'])
app.add_url_rule('/food/lastMeal', view_func=food.queryLastMeal, methods=['GET'])

app.run(debug=True, port=80, host="0.0.0.0")

