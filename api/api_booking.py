from flask import *
from mysql.connector import errorcode
import mysql.connector 
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime
from model.database import DB

# 建立 Flask Blueprint
api_booking = Blueprint("api_booking", __name__)

# 建立 token
load_dotenv()
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
			connection_object = DB.conn_obj()
			mycursor = connection_object.cursor(dictionary=True)
			query = ("""
				SELECT 
					a.id, 
					a.name, 
					a.address, 
					c.date, 
					c.time, 
					c.price, 
					GROUP_CONCAT(i.URL) AS image
				FROM attraction AS a
				INNER JOIN cart AS c ON a.id = c.attraction_id
				INNER JOIN image AS i ON a.id = i.attraction_id
				WHERE member_id = %s
				GROUP BY a.id, c.date, c.time, c.price;
			""")
			mycursor.execute(query, (member_id,))
			results = mycursor.fetchall()
			# 尚無預訂行程
			if not results: 
				return jsonify({"data" : None}),200
			# respose data
			datas = []
			for item in results:
				images = item["image"].split(",")
				date = item["date"].strftime('%Y-%m-%d') # 轉換 datetime.date格式
				data = {
						"attraction" : {
							"id" : item["id"],
							"name" : item["name"],
							"address" : item["address"],
							"image" : images[0],
						},
						"date" : date,
						"time" : item["time"],
						"price" : item["price"],
				}
				datas.append(data)
			
			return jsonify({
						"data": datas
					}),200

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			return jsonify({
				"error": True,
				"data" : "INTERNAL_SERVER_ERROR",             
			}),500

		finally:
			if connection_object.is_connected():
				mycursor.close()
				connection_object.close()

	# 建立預定行程
	if request.method == "POST":
		data = request.get_json()
		attraction_id = data["attractionId"]
		date = data["date"]
		time = data["time"]
		price = data["price"]
		if attraction_id == "" or date == "" or time == "" or price == "":
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
			connection_object = DB.conn_obj()
			mycursor = connection_object.cursor()
			# 確認景點是否重複
			query = ("SELECT attraction_id FROM cart WHERE member_id = %s AND attraction_id = %s")
			mycursor.execute(query, (member_id, attraction_id))
			result = mycursor.fetchone()
			if result:
				return jsonify({
							"error": True,
							"data" : "景點已重複訂購",             
						}),400

			else:
				query = ("""
					INSERT INTO cart (attraction_id, member_id, date, time, price)
					VALUES (%s, %s, %s, %s, %s)
				""")
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
			if connection_object.is_connected():
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
			data = request.get_json()
			attraction_id = data["attractionId"]
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = DB.conn_obj()
			mycursor = connection_object.cursor()
			query = ("DELETE FROM cart WHERE member_id = %s AND attraction_id = %s")
			mycursor.execute(query, (member_id, attraction_id))
			connection_object.commit() 
			return jsonify({
						"ok": True    
					}),200
		except:
			return  jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500
		finally:
			if connection_object.is_connected():
				mycursor.close()
				connection_object.close()
