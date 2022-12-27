from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv

# 建立 Flask Blueprint
api_categories = Blueprint("api_categories", __name__)

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


@api_categories.route("/api/categories")
def categories():
	try:
		connection_object = connection_pool.get_connection()
		mycursor = connection_object.cursor(dictionary=True)
		mycursor.execute("SELECT category FROM attraction GROUP BY category")
		result = mycursor.fetchall()
		categories = []
		for i in result:
			categories.append(i['category'])
		return jsonify({
                        "data" : categories              
                    })		

	except mysql.connector.Error as err:
			print("error while select categories: {}".format(err))
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500	

	finally:
		mycursor.close()
		connection_object.close()