from flask import *
from mysql.connector import errorcode
import mysql.connector 
from model.database import DB

# 建立 Flask Blueprint
api_attraction_id = Blueprint("api_attraction_id", __name__)


@api_attraction_id.route("/api/attraction/<int:attractionId>")
def attractionId(attractionId):
	try:
		connection_object = DB.conn_obj()
		mycursor = connection_object.cursor(dictionary=True)
		# response data
		query = ("""
			SELECT 
				a.name, 
				a.description, 
				a.address, 
				a.transport, 
				a.mrt, 
				a.lat, 
				a.lng, 
				a.category, 
				GROUP_CONCAT(image.URL) AS images 
			FROM attraction AS a 
			INNER JOIN image on a.id = image.attraction_id 
			WHERE a.id = %s  
			GROUP BY a.id
		""")
		mycursor.execute(query, (attractionId,))
		result = mycursor.fetchone()
		if not result:
			return jsonify({
						"error": True,
						"data" : "REQUEST NOT FOUND",             
					}),400
		else:
			images = result["images"].split(",")
			return jsonify({
						"data" : {
							"id" : attractionId,
							"name" : result["name"],
							"category" : result["category"],
							"description" : result["description"],
							"address" : result["address"],
							"transport" : result["transport"],
							"mrt" : result["mrt"],
							"lat" : result["lat"],
							"lng" : result["lng"],
							"images" : images        
							}
						})
	except:
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500
	
	finally:
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()