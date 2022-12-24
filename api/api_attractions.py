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
		if keyword == None:
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor(dictionary=True)
			mycursor.execute("SELECT count(id) AS amount_id FROM attraction")
			id = mycursor.fetchone()
			amount_id = id["amount_id"]
			limit = 12
			amount_page = int(amount_id / limit) + 1
			page = int(request.args.get("page"))
			offset = page * limit
			if page < amount_page:
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
					GROUP BY a.id 
					ORDER BY a.id 
					LIMIT %s OFFSET %s
				""")
				value = (limit, offset)
				mycursor.execute(query, value)
				results = mycursor.fetchall()
				# 建立 response data
				datas = []
				for result in results:
					images = result["images"].split(",")
					data = {
						"id" : result["id"],
						"name" : result["name"],
						"category" : result["category"],
						"description" : result["description"],
						"address" : result["address"],
						"transport" : result["transport"],
						"mrt" : result["mrt"],
						"lat" : result["lat"],
						"lng" : result["lng"], 
						"images" : images,       
					}
					datas.append(data)

				if  amount_page <= page +1: 
					return jsonify({
								"nextpage" : None,
								"data" : datas
								})
				else:
					return jsonify({
								"nextpage" : page + 1,
								"data" : datas
								})
			else:
				return jsonify({
							"error": True,
							"data" : "REQUEST NOT FUND",             
						}),400
		
		
		else:
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor(dictionary=True)
			query = ("SELECT count(id) AS amount_id FROM attraction WHERE name like %s or category = %s")
			value = ('%' + keyword + '%', keyword)
			mycursor.execute(query, value)
			id = mycursor.fetchone()
			amount_id = id['amount_id']
			limit = 12
			amount_page = int(amount_id / limit) + 1
			page = int(request.args.get("page"))
			offset = page * limit
			if amount_id != 0 or page < amount_page:
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
				# response data
				datas = []
				for result in results:
					images = result["images"].split(",")
					data = {
						"id" : result["id"],
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
					datas.append(data)

				if amount_page <= page +1 :
					return jsonify({
								"nextpage" : None,
								"data" : datas
								})
				else:
					return jsonify({
								"nextpage" : page + 1,
								"data" : datas
								})
			else:
				return jsonify({
							"error": True,
							"data" : "REQUEST NOT FUND",             
						}),400

	except: 
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500	
	finally:
		mycursor.close()
		connection_object.close()