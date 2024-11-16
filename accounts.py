import mysql.connector
from mysql.connector import Error

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host='sql.freedb.tech',
        port=3306,
        database='freedb_linkedinsites',
        user='freedb_manny',
        password='deK&Uy4%5*XGnRh'
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ", db_info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to the database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")