from flask import *
from api.api_attractions import api_attractions
from api.api_attraction_id import api_attraction_id
from api.api_categories import api_categories
from api.api_user import api_user
from api.api_user_auth import api_user_auth
from api.api_booking import api_booking
from api.api_orders import api_orders
from api.api_order_id import api_order_id
from api.api_member import api_member
import os


app = Flask(__name__, static_folder = "static", static_url_path = "/static")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

# session secret key
session_pw = os.environ.get("SESSION_PW")
app.secret_key = session_pw 

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
@app.route("/member")
def member():
	return render_template("member.html")
@app.route("/order")
def order():
	return render_template("order.html")


# 註冊Flask Blueprint
app.register_blueprint(api_attractions)
app.register_blueprint(api_attraction_id)
app.register_blueprint(api_categories)
app.register_blueprint(api_user)
app.register_blueprint(api_user_auth)
app.register_blueprint(api_booking)
app.register_blueprint(api_orders)
app.register_blueprint(api_order_id)
app.register_blueprint(api_member)

app.run(host = '0.0.0.0', port = 3000)