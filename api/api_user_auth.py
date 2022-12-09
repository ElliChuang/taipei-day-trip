from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv
import jwt
import datetime
from werkzeug.security import check_password_hash

# 建立 Flask Blueprint
api_user_auth = Blueprint("api_user_auth", __name__)

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



@api_user_auth.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def user_auth():
	# 取得當前會員資訊
	if request.method == "GET":
		if "token" in session:
			try:
				token = session["token"]
				decodeData = jwt.decode(token, token_pw, algorithms="HS256")
				return jsonify({
						"data": {
								"id" : decodeData["id"],
								"name" : decodeData["name"],
								"email" : decodeData["email"],
							}
						}),200
			except:
				return jsonify({"data": "token is not valid."})
		else:
			print("no token in session")
			return jsonify({"data": None}),400

	# 使用者登入
	if request.method == "PUT":
		data = request.get_json()
		email = data["email"]
		password = data["password"]
		print("登入取得：", data)
		if email == "" or password == "":
			return jsonify({
						"error": True,
						"data" : "請輸入電子郵件及密碼",             
					}),400
		try:
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor()
			query = ("SELECT id, email, password FROM member where email = %s")
			mycursor.execute(query, (email,))
			result = mycursor.fetchone()
			print("登入取得資料庫：", result)
			if not result: 
				return jsonify({
							"error": True,
							"data" : "電子郵件輸入錯誤",             
						}),400
			elif check_password_hash(result[2], password):
				payload = {
					"id" : result[0],
					"name" : result[1],
					"email" : result[2],
					'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
				}
				token = jwt.encode(payload, token_pw, algorithm="HS256")
				session["token"] = token
				print("token:ok")
				return jsonify({
							"ok": True    
						}),200
			else:
				return jsonify({
							"error": True,
							"data" : "密碼輸入錯誤",             
						}),400

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			return jsonify({
				"error": True,
				"data" : "INTERNAL_SERVER_ERROR",             
			}),500

		finally:
			mycursor.close()
			connection_object.close()


	# 登出會員
	if request.method == "DELETE":
		try:
			session.pop("token", None)
			return jsonify({
						"ok": True    
					}),200
		except:
			return  jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500
