from flask import Flask
import mysql.connector 
from mysql.connector import pooling 
from mysql.connector import errorcode
import json

json_data = open("data/taipei-attractions.json").read()
json_obj = json.loads(json_data)
datas = json_obj["result"]["results"]

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

# 抓出九大類景點
types = set()
for data in datas:
    type = data["CAT"]
    types.add(type)

ans = {}
i = 1
for type in types:
    ans[type] = i
    i += 1 

def category():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        # 回傳db 
        for i in types:
            query = "INSERT INTO category (category) VALUES (%s)"
            value = i
            mycursor.execute(query, (value,))
            connection_object.commit()
    except mysql.connector.Error as err:
        print("Unexcepted Error", err)
    finally:
        mycursor.close()
        connection_object.close()

def attraction():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        for data in datas:
            id = data["_id"]
            name = data["name"]
            description = data["description"]
            address = data["address"]
            transport = data["direction"]
            MRT = data["MRT"]
            lat = data["latitude"]
            lng = data["longitude"]
            CAT = data["CAT"]
            category_id = ans[CAT]
            # 回傳db 
            query = "INSERT INTO attraction (id, name, description, address, transport, MRT, lat, lng, category_id) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            value = (id, name, description, address, transport, MRT, lat, lng, category_id)
            mycursor.execute(query, value)
            connection_object.commit()

    except mysql.connector.Error as err:
        print("Unexcepted Error", err)
    finally:
        mycursor.close()
        connection_object.close()
        

def image():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        for data in datas:
            images = data["file"].split("https://")
            id = data["_id"]
            for image in images:
                if "jpg" in image or "JPG" in image or "png"in image or "PNG" in image :             
                    image_url = "https://" + image
                    # print(image_url)
                    # 回傳db 
                    query = "INSERT INTO image (URL, attraction_id) VALUES ( %s, %s)"
                    value = (image_url, id)
                    # print(value)
                    mycursor.execute(query, value)
                    connection_object.commit()

    except mysql.connector.Error as err:
        print("Unexcepted Error", err)
    finally:
        mycursor.close()
        connection_object.close()






# attraction()
# category()
# image()

