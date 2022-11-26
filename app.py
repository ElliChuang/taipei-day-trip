from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import json
import os
from dotenv import load_dotenv

load_dotenv()
db_pw = os.environ.get("DB_PW")

app=Flask(__name__, static_folder="static", static_url_path="/static")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

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

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



@app.route("/api/attractions")
def attractions():
	try:
		keyword = request.args.get("keyword")
		if keyword == None:
			connection_object = connection_pool.get_connection()
			mycursor = connection_object.cursor()
			mycursor.execute("SELECT count(id) FROM attraction")
			id = mycursor.fetchone()
			amount_id = id[0]
			limit = 12
			amount_page = int(amount_id / limit) + 1
			page = int(request.args.get("page"))
			offset = page * limit
			if page < amount_page:
				query = (
					"SELECT a.id, a.name, a.description, a.address, a.transport, a.mrt, a.lat, a.lng, a.category, GROUP_CONCAT(image.URL) "
					"FROM attraction AS a "
					"INNER JOIN image on a.id = image.attraction_id "
					"GROUP BY a.id "
					"ORDER BY a.id "
					"LIMIT %s OFFSET %s"
					)
				value = (limit, offset)
				mycursor.execute(query, value)
				results = mycursor.fetchall()
				# 建立 response data
				datas = []
				for result in results:
					images = result[9].split(",")
					data = {
						"id" : result[0],
						"name" : result[1],
						"category" : result[8],
						"description" : result[2],
						"address" : result[3],
						"transport" : result[4],
						"mrt" : result[5],
						"lat" : result[6],
						"lng" : result[7], 
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
			mycursor = connection_object.cursor()
			query = ("SELECT count(id) FROM attraction WHERE name like %s or category = %s")
			value = ('%' + keyword + '%', keyword)
			mycursor.execute(query, value)
			id = mycursor.fetchone()
			amount_id = id[0]
			limit = 12
			amount_page = int(amount_id / limit) + 1
			page = int(request.args.get("page"))
			offset = page * limit
			if amount_id != 0 or page < amount_page:
				query = (
					"SELECT a.id, a.name, a.description, a.address, a.transport, a.mrt, a.lat, a.lng, a.category, GROUP_CONCAT(image.URL) " 
					"FROM attraction AS a "
					"INNER JOIN image on a.id = image.attraction_id " 
					"WHERE name like %s or category = %s "
					"GROUP BY a.id "
					"ORDER BY a.id " 
					"LIMIT %s OFFSET %s"
					)
				value = ('%' + keyword + '%', keyword, limit, offset)
				mycursor.execute(query, value)
				results = mycursor.fetchall()
				# response data
				datas = []
				for result in results:
					images = result[9].split(",")
					data = {
						"id" : result[0],
						"name" : result[1],
						"category" : result[8],
						"description" : result[2],
						"address" : result[3],
						"transport" : result[4],
						"mrt" : result[5],
						"lat" : result[6],
						"lng" : result[7], 
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




@app.route("/api/attraction/<int:attractionId>")
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



@app.route("/api/categories")
def categories():
	try:
		connection_object = connection_pool.get_connection()
		mycursor = connection_object.cursor()
		mycursor.execute("SELECT category FROM attraction GROUP BY category")
		result = mycursor.fetchall()
		categories = []
		for i in result:
			categories.append(i[0])
		return jsonify({
                        "data" : categories              
                    })		
	except: 
			return jsonify({
						"error": True,
						"data" : "INTERNAL_SERVER_ERROR",             
					}),500	
	finally:
		mycursor.close()
		connection_object.close()





app.run(host='0.0.0.0', port=3000)