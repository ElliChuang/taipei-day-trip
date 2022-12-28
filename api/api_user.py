from flask import *
from mysql.connector import errorcode
import mysql.connector 
from werkzeug.security import generate_password_hash
from model.database import DB

# 建立 Flask Blueprint
api_user = Blueprint("api_user", __name__)


@api_user.route("/api/user", methods=["POST"])
def signup():
	data = request.get_json()
	if data["name"] == "" or data["email"] == "" or data["password"] == "":
		return jsonify({
					"error": True,
					"data" : "請輸入姓名、電子郵件及密碼",             
				}),400
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor()
		query = ("SELECT email FROM member where email = %s")
		mycursor.execute(query, (data["email"],))
		result = mycursor.fetchone()
		if result:
			return jsonify({
						"error": True,
						"data" : "電子郵件已被註冊",             
					}),400
		else: 
			# 將使用者密碼加密
			hash_password = generate_password_hash(data['password'], method='sha256')
			query = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
			value = (data["name"], data["email"], hash_password)
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