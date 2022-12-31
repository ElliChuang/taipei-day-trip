from flask import *
from mysql.connector import errorcode
import mysql.connector 
# from mysql.connector import pooling 
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime
import requests
import random
import json
from model.database import DB

# 建立 Flask Blueprint
api_orders = Blueprint("api_orders", __name__)

load_dotenv()
# db_pw = os.environ.get("DB_PW")
token_pw = os.environ.get("TOKEN_PW")
partner_key = os.environ.get("PARTNER_KEY")


@api_orders.route("/api/orders", methods=["POST"])
def order():
	# 建立新的訂單＆付款
	if "token" not in session:
		return jsonify({
					"error": True,
					"data" : "請先登入會員",             
				}),403
	data = request.get_json()
	total_amount = data["order"]["amount"]
	trip = data["order"]["trip"]
	contact = data["order"]["contact"]
	prime = data["prime"]
	status = "未付款"
	order_time = datetime.now().strftime('%Y%m%d')
	order_num = random.randrange(1000,9999)
	order_id = order_time + str(order_num)
	# 訂單建立失敗
	if contact["name"] == "" or contact["email"] == "" or len(contact["phone"]) != 10 or prime == "" or len(trip) == 0:
		return jsonify({
					"error": True,
					"data" : "訂單資訊填寫不全",             
				}),400
	
	token = session["token"]
	decode_data = jwt.decode(token, token_pw, algorithms="HS256")
	member_id = decode_data["id"]
	# 建立訂單：insert into orders table
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor()
		orders_query = ("""
			INSERT INTO orders (id, member_id, total_amount, status)
			VALUES (%s, %s, %s, %s)
		""")
		orders_value = (order_id, member_id, total_amount, status)
		mycursor.execute(orders_query, orders_value)
		connection_object.commit() 

	except mysql.connector.Error as err:
			print("error while insert into orders table: {}".format(err))
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500

	finally:
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()
	
	# 建立訂單：insert into order_details table	
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor()
		for i in trip:
			attraction_id = i["attraction"]["id"]
			date = i["date"]
			time = i["time"]
			price = i["price"]
			order_details_query = ("""
				INSERT INTO order_details (
					order_id,
					attraction_id,
					date, 
					time, 
					price, 
					contact)
				VALUES (%s, %s, %s, %s, %s, %s)
			""")
			order_details_value = (order_id, attraction_id, date, time, price, json.dumps(contact, ensure_ascii = False))
			mycursor.execute(order_details_query, order_details_value)
			connection_object.commit() 

	except mysql.connector.Error as err:
		print("error while insert into order_details table: {}".format(err))
		return jsonify({
					"error": True,
					"data" : "INTERNAL_SERVER_ERROR",             
				}),500

	finally:
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()

	# 已成立的訂單，刪除 cart items
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor()
		query = ("DELETE FROM cart WHERE member_id = %s")
		mycursor.execute(query, (member_id,))
		connection_object.commit() 	

	except mysql.connector.Error as err:
		print("error while delete cart items: {}".format(err))
		return jsonify({
					"error": True,
					"data" : "INTERNAL_SERVER_ERROR",             
				}),500

	finally:
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()

	# 發 prime 給 TapPay 付款
	url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
	merchant_id = "elli8208_CTBC"
	headers = {
			'Content-Type' : 'application/json',
			'x-api-key' : partner_key
	}
	data = {			
		"prime": prime,
		"partner_key": partner_key,
		"merchant_id": merchant_id,
		"details": "訂單編號：" + order_id,
		"amount": total_amount,
		"cardholder": {
			"phone_number": contact["phone"],
			"name": contact["name"],
			"email": contact["email"],
		},
		"remember": True
	}
	response = requests.post(url, headers = headers, data = json.dumps(data))
	result = response.json()
	prime_status = result["status"]
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor()
		if (prime_status != 0):
			query = ("""
				INSERT INTO payment (order_id, status)
				VALUES (%s, %s)
			""")
			value = (order_id, "付款失敗")
			mycursor.execute(query, value)
			connection_object.commit() 
			return jsonify({
						"data": {
							"number": order_id,
							"payment": {
								"status": prime_status,
								"message": "付款失敗"
								}
						}
					}),200

		elif (prime_status == 0):
			payment_query = ("""
				INSERT INTO payment (order_id, status)
				VALUES (%s, %s)
			""")
			payment_value = (order_id, "付款成功")
			mycursor.execute(payment_query, payment_value)
			connection_object.commit() 
			# 更新 orders table 的狀態
			orders_query = ("""
				UPDATE orders SET status = %s 
				WHERE id = %s
			""")
			orders_value = ("已付款", order_id)
			mycursor.execute(orders_query, orders_value)
			connection_object.commit() 
			return jsonify({
						"data": {
							"number": order_id,
							"payment": {
								"status": prime_status,
								"message": "付款成功"
								}
						}
					}),200

	except mysql.connector.Error as err:
		print("error while insert into payment table: {}".format(err))
		return jsonify({
					"error": True,
					"data" : "INTERNAL_SERVER_ERROR",             
				}),500

	finally:
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()


@api_orders.route("/api/orders", methods=["GET"])
def getOrders():
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
				created_dt AS order_dt,	 
				id AS order_id,
				status,
				total_amount AS price 
			FROM orders
			WHERE member_id = %s
		""")
		mycursor.execute(query, (member_id,))
		results = mycursor.fetchall()
		# 尚無預訂行程
		if not results: 
			return jsonify({"data" : None}),200
		# respose data
		datas = []
		for item in results:
			date = item["order_dt"].strftime('%Y-%m-%d') # 轉換 datetime.date格式
			data = {
					"order_dt" : date,
					"order_id" : item["order_id"],
					"status" : item["status"],
					"price" : item["price"]
				}
			
			datas.append(data)
		print(datas)
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