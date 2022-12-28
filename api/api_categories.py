from flask import *
from mysql.connector import errorcode
import mysql.connector 
from model.database import DB

# 建立 Flask Blueprint
api_categories = Blueprint("api_categories", __name__)


@api_categories.route("/api/categories")
def categories():
	try:
		connection_object = DB.conn_obj()
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
		if connection_object.is_connected():
			mycursor.close()
			connection_object.close()