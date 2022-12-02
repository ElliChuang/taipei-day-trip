from flask import *
from api.api_attractions import api_attractions
from api.api_attraction_id import api_attraction_id
from api.api_categories import api_categories


app = Flask(__name__, static_folder = "static", static_url_path = "/static")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


# 註冊Flask Blueprint
app.register_blueprint(api_attractions)
app.register_blueprint(api_attraction_id)
app.register_blueprint(api_categories)


app.run(host = '0.0.0.0', port = 3000)