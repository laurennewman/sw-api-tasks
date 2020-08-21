import mysql.connector

# Specify your server connection here.
try:
	db_cnx = mysql.connector.connect(user="username", password="password",
    host="localhost", auth_plugin="mysql_native_password")
except:
    print("Could not connect to the server...")
    raise

db_cursor = db_cnx.cursor()

db_cursor.execute("CREATE DATABASE IF NOT EXISTS swapi_tasks")

db_cnx.connect(database="swapi_tasks")

db_cursor.execute("DROP TABLE IF EXISTS people")
db_cursor.execute("CREATE TABLE IF NOT EXISTS people \
    (id INT NOT NULL PRIMARY KEY, name VARCHAR(255) NOT NULL)")

db_cursor.execute("DROP TABLE IF EXISTS films")
db_cursor.execute("CREATE TABLE IF NOT EXISTS films \
    (id INT NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL)")

db_cursor.execute("DROP TABLE IF EXISTS people_in_films")
db_cursor.execute("CREATE TABLE IF NOT EXISTS people_in_films \
    (people_id INT NOT NULL, film_id INT NOT NULL)")

db_cnx.close()
