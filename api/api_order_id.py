from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime
import json

# 建立 Flask Blueprint
api_order_id = Blueprint("api_order_id", __name__)

load_dotenv()
db_pw = os.environ.get("DB_PW")
token_pw = os.environ.get("TOKEN_PW")

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


@api_order_id.route("/api/order/<int:orderNumber>", methods=["GET"])
def getOrderNumber(orderNumber):
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
		mycursor = connection_object.cursor(dictionary=True)
		# 確認景點是否重複
		query = ("""
			SELECT 
				d.attraction_id, 
				d.date, 
				d.time, 
				d.price, 
				d.contact, 
				a.name, 
				a.address, 
				GROUP_CONCAT(i.URL) AS image,
					(
						SELECT total_amount 
						FROM orders 
						WHERE member_id = %s AND id = %s
						) AS total_amount,
					(
						SELECT status 
						FROM orders 
						WHERE member_id = %s AND id = %s
						) AS status
			FROM order_details AS d
			INNER JOIN orders AS o ON d.order_id = o.id
			INNER JOIN attraction AS a ON d.attraction_id = a.id
			INNER JOIN image AS i ON i.attraction_id = a.id
			WHERE o.member_id = %s AND o.id = %s
			GROUP BY d.attraction_id, d.date, d.time, d.price, d.contact;
		""")
		mycursor.execute(query, (member_id, orderNumber, member_id, orderNumber, member_id, orderNumber))
		results = mycursor.fetchall()
		# 查無訂單
		if not results:
			return jsonify({
						"data" : None,             
					}),200
		# 取得 response data
		total_amount = results[0]["total_amount"]
		contact = json.loads(results[0]["contact"]) # convert string to dict
		status = ""; 
		if results[0]["status"] == "已付款":
			status = 0
		else: 
			status = 1
		trip = []
		for item in results:
			images = item["image"].split(",")
			date = item["date"].strftime('%Y-%m-%d') 
			data = {
					"attraction" : {
						"id" : item["attraction_id"],
						"name" : item["name"],
						"address" : item["address"],
						"image" : images[0],
					},
					"date" : date,
					"time" : item["time"],
					"price" : item["price"],
					"status" : status,
			}
			trip.append(data)
		return jsonify({
					"data":{
						"number" : orderNumber,
						"total_amount" : total_amount,
						"trip" : trip,
						"contact" : contact,
					}
				}),200

	except mysql.connector.Error as err:
		print("error while select the orderNumber: {}".format(err))
		return jsonify({
					"error": True,
					"data" : "INTERNAL_SERVER_ERROR",             
				}),500

	finally:
		mycursor.close()
		connection_object.close()