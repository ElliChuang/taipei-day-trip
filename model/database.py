import mysql.connector 
from mysql.connector import pooling 
import os
from dotenv import load_dotenv

class DB:
    def conn_obj():
        # password
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
            pool_size = 32,
            pool_reset_session = True,
            **dbconfig
        )

        # 連線
        connection_object = connection_pool.get_connection()

        return connection_object
    



