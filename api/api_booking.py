from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv
import jwt


# 建立 Flask Blueprint
api_booking = Blueprint("api_booking", __name__)

load_dotenv()
db_pw = os.environ.get("DB_PW")

# 建立db
dbconfig = {
    "user" : "root",
    "password" : db_pw,
    "host" : "localhost",
    "database" : "taipei_day_trip",
}
# create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "taipei_pool",
    pool_size = 5,
    pool_reset_session = True,
    **dbconfig
)

# 建立 token
token_pw = os.environ.get("TOKEN_PW")


@api_booking.route("/api/booking", methods=["GET", "POST", "DELETE"])
def booking():
	# 取得訂購資訊
	if request.method == "GET":
		if "token" not in session:
			return jsonify({
						"error": True,
						"data" : "請先登入會員",             
					}),403
		try:
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor()
			query = ("""
				SELECT a.id, a.name, a.address, c.date, c.time, c.price,
					(
						SELECT GROUP_CONCAT(i.URL)
						FROM attraction AS a
						INNER JOIN image AS i ON a.id = i.attraction_id
						WHERE a.id = (
							SELECT attraction_id 
							FROM cart 
							WHERE member_id = 9
							) 
						GROUP BY a.id
					) AS URL
				FROM attraction AS a
				INNER JOIN cart AS c 
				ON a.id = c.attraction_id
				WHERE a.id = (
					SELECT attraction_id 
					FROM cart 
					WHERE member_id = %s
					)
			""")
			mycursor.execute(query, (member_id,))
			result = mycursor.fetchone()
			images = result[6].split(",") 
			return jsonify({
					"data": {
							"attraction" : {
								"id" : result[0],
								"name" : result[1],
								"address" : result[2],
								"image" : images[0],
							},
							"date" : result[3],
							"time" : result[4],
							"price" : result[5],
						}
					}),200
		except:
			return jsonify({"data": "token is not valid."})


	# 建立預定行程
	if request.method == "POST":
		data = request.get_json()
		attraction_id = data["attractionId"]
		date = data["date"]
		time = data["time"]
		price = data["price"]
		if attraction_id == "" or data == "" or time == "" or price == "":
			return jsonify({
						"error": True,
						"data" : "請選擇日期及時間",             
					}),400
		if "token" not in session:
			return jsonify({
						"error": True,
						"data" : "請先登入會員",             
					}),403
		try:
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor()
			query = (
				"INSERT INTO cart (attraction_id, member_id, date, time, price)" 
				"VALUES (%s, %s, %s, %s, %s)"
				)
			value = (attraction_id, member_id, date, time, price)
			mycursor.execute(query, value)
			connection_object.commit() 
			return jsonify({
						"ok": True,          
					}),200

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			return jsonify({
				"error": True,
				"data" : "INTERNAL_SERVER_ERROR",             
			}),500

		finally:
			mycursor.close()
			connection_object.close()


	# 刪除行程
	if request.method == "DELETE":
		if "token" not in session:
			return jsonify({
						"error": True,
						"data" : "請先登入會員",             
					}),403
		try:
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor()
			query = ("DELETE FROM cart WHERE member_id = %s")
			mycursor.execute(query, (member_id,))
			connection_object.commit() 
			return jsonify({
						"ok": True    
					}),200
		except:
			return  jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500
