from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv

# 建立 Flask Blueprint
api_attraction_id = Blueprint("api_attraction_id", __name__)

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


@api_attraction_id.route("/api/attraction/<int:attractionId>")
def attractionId(attractionId):
	try:
		connection_object = connection_pool.get_connection()
		mycursor = connection_object.cursor()
		# id
		mycursor.execute("SELECT id FROM attraction")
		ids = mycursor.fetchall()
		result_id = []
		for id in ids:
			result_id.append(id[0])
		# response data
		query = (
			"SELECT a.name, a.description, a.address, a.transport, a.mrt, a.lat, a.lng, a.category, GROUP_CONCAT(image.URL) " 
			"FROM attraction AS a " 
			"INNER JOIN image on a.id = image.attraction_id " 
			"WHERE a.id = %s " 
			"GROUP BY a.id"
			)
		mycursor.execute(query, (attractionId,))
		result = mycursor.fetchone()
		images = result[8].split(",")
		if attractionId not in result_id:
			return jsonify({
						"error": True,
						"data" : "REQUEST NOT FUND",             
					}),400
		else:
			return jsonify({
						"data" : {
							"id" : attractionId,
							"name" : result[0],
							"category" : result[7],
							"description" : result[1],
							"address" : result[2],
							"transport" : result[3],
							"mrt" : result[4],
							"lat" : result[5],
							"lng" : result[6],
							"images" : images        
							}
						})
	except:
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500
	
	finally:
		mycursor.close()
		connection_object.close()