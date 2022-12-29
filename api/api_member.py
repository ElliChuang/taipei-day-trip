from flask import *
from mysql.connector import errorcode
import mysql.connector 
from werkzeug.security import generate_password_hash, check_password_hash
from model.database import DB
import os
from dotenv import load_dotenv
import jwt
import datetime

# 建立 Flask Blueprint
api_member = Blueprint("api_member", __name__)

# 建立 token
load_dotenv()
token_pw = os.environ.get("TOKEN_PW")

@api_member.route("/api/member", methods=["PATCH"])
def modify_infor():
	if "token" not in session:
		return jsonify({
					"error": True,
					"data" : "請先登入會員",             
				}),403

	data = request.get_json()
	if "name" in data.keys():
		if data["name"] == "" or data["email"] == "":
			return jsonify({
						"error": True,
						"data" : "請輸入姓名及電子郵件",             
					}),400

		try:
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = DB.conn_obj()
			mycursor = connection_object.cursor()
			query = ("UPDATE member SET name = %s, email = %s WHERE id = %s")
			value = (data["name"], data["email"], member_id)
			mycursor.execute(query, value)
			connection_object.commit() 
			# 更新token
			payload = {
				"id" : member_id,
				"name" : data["name"],
				"email" : data["email"],
				'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7)
			}
			token = jwt.encode(payload, token_pw, algorithm="HS256")
			session["token"] = token
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
	
	elif "password" in data.keys():
		if data["password"] == "" or data["newPassword"] == "" or data["checkPassword"] == "":
			return jsonify({
						"error": True,
						"data" : "請輸入密碼",             
					}),400
		if  data["newPassword"] != data["checkPassword"]:
			return jsonify({
						"error": True,
						"data" : "新密碼不一致",             
					}),400
		try:
			token = session["token"]
			decode_data = jwt.decode(token, token_pw, algorithms="HS256")
			member_id = decode_data["id"]
			connection_object = DB.conn_obj()
			mycursor = connection_object.cursor(dictionary=True)
			query = ("SELECT password FROM member WHERE id = %s")
			mycursor.execute(query, (member_id,))
			result = mycursor.fetchone()
			
			if check_password_hash(result["password"], data["password"]):
				hash_password = generate_password_hash(data["newPassword"], method='sha256')
				query = ("UPDATE member SET password = %s WHERE id = %s")
				value = (hash_password, member_id)
				mycursor.execute(query, value)
				connection_object.commit() 
				return jsonify({
							"ok": True,          
						}),200
			else:
				return jsonify({
							"error": True,
							"data" : "原密碼輸入錯誤",             
						}),400

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