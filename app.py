from flask import *
from mysql.connector import errorcode
import mysql.connector 
from mysql.connector import pooling 
import json
# from werkzeug.exceptions import HTTPException

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

# 建立db
dbconfig = {
    "user" : "root",
    "password" : "",
    "host" : "localhost",
    "database" : "stage2",
}
# create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "stage2_pool",
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
				query = ("SELECT id, name, description, address, transport, mrt, lat, lng FROM attraction ORDER BY id LIMIT %s OFFSET %s")
				value = (limit, offset)
				mycursor.execute(query, value)
				results = mycursor.fetchall()
				datas = []
				for result in results:
					# image
					image_query = ("SELECT URL FROM image WHERE attraction_id = %s")
					mycursor.execute(image_query, (result[0],))
					images = mycursor.fetchall()
					result_image = []
					for image in images:
						result_image.append(image[0])
					# category
					category_query = ("SELECT category.category FROM category INNER JOIN attraction on attraction.category_id = category.id WHERE attraction.id = %s")
					mycursor.execute(category_query, (result[0],))
					result_category = mycursor.fetchone()
					# 建立 response data
					data = {
						"id" : result[0],
						"name" : result[1],
						"category" : result_category[0],
						"description" : result[2],
						"address" : result[3],
						"transport" : result[4],
						"mrt" : result[5],
						"lat" : result[6],
						"lng" : result[7], 
						"images" : result_image,       
					}
					datas.append(data)

				if page +1 == amount_page:
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
			query = ("SELECT count(attraction.id) FROM attraction INNER JOIN category on attraction.category_id = category.id WHERE attraction.name like %s or category.category = %s")
			value = ('%' + keyword + '%', keyword)
			mycursor.execute(query, value)
			id = mycursor.fetchone()
			amount_id = id[0]
			limit = 12
			amount_page = int(amount_id / limit) + 1
			page = int(request.args.get("page"))
			offset = page * limit
			if page < amount_page:
				query = ("SELECT a.id, a.name, a.description, a.address, a.transport, a.mrt, a.lat, a.lng FROM attraction AS a INNER JOIN category on a.category_id = category.id WHERE a.name like %s or category.category = %s ORDER BY a.id LIMIT %s OFFSET %s")
				value = ('%' + keyword + '%', keyword, limit, offset)
				mycursor.execute(query, value)
				results = mycursor.fetchall()
				datas = []
				for result in results:
					# image
					image_query = ("SELECT URL FROM image WHERE attraction_id = %s")
					mycursor.execute(image_query, (result[0],))
					images = mycursor.fetchall()
					result_image = []
					for image in images:
						result_image.append(image[0])
					# category
					category_query = ("SELECT category.category FROM category INNER JOIN attraction on attraction.category_id = category.id WHERE attraction.id = %s")
					mycursor.execute(category_query, (result[0],))
					result_category = mycursor.fetchone()
					# 建立 response data
					data = {
						"id" : result[0],
						"name" : result[1],
						"category" : result_category[0],
						"description" : result[2],
						"address" : result[3],
						"transport" : result[4],
						"mrt" : result[5],
						"lat" : result[6],
						"lng" : result[7], 
						"images" : result_image,       
					}
					datas.append(data)

				if page +1 == amount_page:
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
		# image
		image_query = ("SELECT URL FROM image WHERE attraction_id = %s")
		mycursor.execute(image_query, (attractionId,))
		images = mycursor.fetchall()
		result_image = []
		for image in images:
			result_image.append(image[0])
		# category
		category_query = ("SELECT category.category FROM category INNER JOIN attraction on attraction.category_id = category.id WHERE attraction.id = %s")
		mycursor.execute(category_query, (attractionId,))
		result_category = mycursor.fetchone()
		# else
		query = ("SELECT name, description, address, transport, mrt, lat, lng FROM attraction WHERE id = %s")
		mycursor.execute(query, (attractionId,))
		result = mycursor.fetchone()
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
							"category" : result_category[0],
							"description" : result[1],
							"address" : result[2],
							"transport" : result[3],
							"mrt" : result[4],
							"lat" : result[5],
							"lng" : result[6],
							"images" : result_image              
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
		mycursor.execute("SELECT category FROM category")
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





app.run(port=3000)