import logging
from os import environ

import mysql.connector

logging.basicConfig(level=environ["LOG_LEVEL"])


def connect_to_mysql():
    try:
        logging.debug("Connecting to MySQL server")
        db_cnx = mysql.connector.connect(user=environ["MYSQL_USER"],
                                         password=environ["MYSQL_PASSWORD"],
                                         host=environ["MYSQL_HOST"],
                                         auth_plugin=environ["MYSQL_AUTH_PLUGIN"])
        return db_cnx, db_cnx.cursor()
    except mysql.connector.Error as e:
        logging.error(f"Something went wrong: {e}")
        raise


def create_database(db_cursor):
    try:
        logging.debug("Creating database if it does not exist")
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS swapi_tasks")
        db_cursor.execute("USE swapi_tasks")

        logging.debug("Dropping and creating tables")
        db_cursor.execute("DROP TABLE IF EXISTS characters")
        db_cursor.execute("CREATE TABLE IF NOT EXISTS characters \
            (id INT NOT NULL PRIMARY KEY, name VARCHAR(255) NOT NULL)")

        db_cursor.execute("DROP TABLE IF EXISTS films")
        db_cursor.execute("CREATE TABLE IF NOT EXISTS films \
            (id INT NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL)")

        db_cursor.execute("DROP TABLE IF EXISTS characters_in_films")
        db_cursor.execute("CREATE TABLE IF NOT EXISTS characters_in_films \
            (character_id INT NOT NULL, film_id INT NOT NULL)")
    except mysql.connector.Error as e:
        logging.error(f"Something went wrong: {e}")
        raise


def execute_sql(db_cursor, sql):
    try:
        db_cursor.execute(sql)
    except mysql.connector.Error as e:
        logging.error(f"Something went wrong: {e}")
        raise


def count_characters(db_cursor):
    sql = "SELECT COUNT(*) FROM characters"
    execute_sql(db_cursor, sql)
    (character_count,) = db_cursor.fetchone()
    logging.debug(f"Counted {character_count} characters")
    return character_count


def insert_character(db_cursor, character_id, name):
    logging.debug(f"Inserting  character id {character_id} to the database")
    sql = f"INSERT INTO characters (id, name) VALUES ('{character_id}','{name}')"
    execute_sql(db_cursor, sql)


def insert_characters_in_films(db_cursor, character_id, film_id):
    logging.debug(f"Inserting character id {character_id} and film id {film_id} to the database")
    sql = f"INSERT INTO characters_in_films (character_id, film_id) VALUES ('{character_id}','{film_id}')"
    execute_sql(db_cursor, sql)


def select_film_ids(db_cursor):
    sql = "SELECT DISTINCT film_id FROM characters_in_films"
    execute_sql(db_cursor, sql)
    return db_cursor.fetchall()


def insert_film(db_cursor, film_id, title):
    logging.debug(f"Inserting film id {film_id} to the database")
    sql = f"INSERT INTO films (id, title) VALUES ('{film_id}','{title}')"
    execute_sql(db_cursor, sql)


def select_films(db_cursor):
    sql = "SELECT * FROM films"
    execute_sql(db_cursor, sql)
    return db_cursor.fetchall()


def select_characters_in_films(db_cursor, film_id):
    sql = f"SELECT c.name FROM characters_in_films cif \
            LEFT JOIN characters c ON cif.character_id = c.id \
            WHERE cif.film_id = {film_id}"
    execute_sql(db_cursor, sql)
    return db_cursor.fetchall()
