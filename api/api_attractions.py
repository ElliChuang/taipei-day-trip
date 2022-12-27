from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv

# 建立 Flask Blueprint
api_attractions = Blueprint("api_attractions", __name__)

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


@api_attractions.route("/api/attractions")
def attractions():
	try:
		keyword = request.args.get("keyword")
		connection_object = connection_pool.get_connection()
		mycursor = connection_object.cursor(dictionary=True)
		limit = 13
		page = int(request.args.get("page"))
		offset = page * (limit-1)
		query = ("""
			SELECT 
				a.id,
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
			WHERE name like %s or category = %s 
			GROUP BY a.id 
			ORDER BY a.id 
			LIMIT %s OFFSET %s
		""")					
		value = ('%' + keyword + '%', keyword, limit, offset)
		mycursor.execute(query, value)
		results = mycursor.fetchall()
		if not results:
			return jsonify({
						"error": True,
						"data" : "REQUEST NOT FUND",             
						}),400
		
		if len(results) < 13:
			# response data
			datas = []
			for i in range(len(results)):
				images = results[i]["images"].split(",")
				data = {
					"id" : results[i]["id"],
					"name" : results[i]["name"],
					"category" : results[i]["category"],
					"description" : results[i]["description"],
					"address" : results[i]["address"],
					"transport" : results[i]["transport"],
					"mrt" : results[i]["mrt"],
					"lat" : results[i]["lat"],
					"lng" : results[i]["lng"], 
					"images" : images      
				}
				datas.append(data)
			print('datas:', len(datas))
			return jsonify({
						"nextpage" : None,
						"data" : datas
						})
		else:
			# response data
			datas = []
			for i in range(len(results)-1):
				images = results[i]["images"].split(",")
				data = {
					"id" : results[i]["id"],
					"name" : results[i]["name"],
					"category" : results[i]["category"],
					"description" : results[i]["description"],
					"address" : results[i]["address"],
					"transport" : results[i]["transport"],
					"mrt" : results[i]["mrt"],
					"lat" : results[i]["lat"],
					"lng" : results[i]["lng"], 
					"images" : images      
				}
				datas.append(data)
			print('datas:', len(datas))
			return jsonify({
						"nextpage" : page + 1,
						"data" : datas
						})

	except: 
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500	
	finally:
		mycursor.close()
		connection_object.close()