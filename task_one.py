import logging
import datetime
import requests
import json
import mysql.connector
import random

# Specify your database connection here.
try:
    db_cnx = mysql.connector.connect(user='username', password='password', 
        host='localhost', database='swapi_tasks', 
        auth_plugin='mysql_native_password')
except:
    print("Could not connect to the database...")
    raise

db_cursor = db_cnx.cursor()

random_num_list : list = []

logging.basicConfig(filename="task_one.log",level=logging.DEBUG)

def count_ppl():
    db_cursor.execute("SELECT COUNT(*) FROM people")
    (ppl,) = db_cursor.fetchone()
    logging.debug("Counted " + str(ppl) + " people.")
    return ppl

def generate_random_num():
    try:
        rando_is_unique : bool = False
        while rando_is_unique == False:
            rando : int = random.randint(1,87)
            logging.debug("Generated random number " + str(rando) + ".")
            rando_is_unique = check_random_num(rando)
        random_num_list.append(rando)
        return rando
    except Exception as e:
        logging.error("Something went wrong in the generate_random_num "
            "function...")
        raise e

def check_random_num(random_num):
    try:
        if random_num in random_num_list:
            logging.debug("Random number " + str(random_num) + " is not "
                "unique.")
            return False
        else:
            logging.debug("Random number " + str(random_num) + " is unique.")
            return True
    except Exception as e:
        logging.error("Something went wrong in the check_random_num "
            "function...")
        raise e

def get_people(random_num):
    try:
        # Assemble url.
        url : str = "https://swapi.co/api/people/" + str(random_num) + "/"
        
        # Hit the GET /people/ endpoint.
        response = requests.get(url)

        # Check if status_code is OK.
        if response.status_code == 200:
            data = response.json()
            name : str = data["name"]
        
            # Save people to the people table.
            logging.debug("Saving people_id " + str(random_num) + ", " 
                + name + " to the people table...")
            save_people(random_num, name)

            # Iterate through films.
            films : list = data["films"]
            for film in films:
                film_id : int = (film[len("https://swapi.co/api/films/"):
                    len(film)-1])
                
                # Save films that people were in to relationship table.
                logging.debug("Saving people_id " + str(random_num) 
                    + " and film_id " + str(film_id) 
                    + " to the people_in_films table...")
                save_people_in_films(random_num, film_id)
        else:
            # We need a new random number because you probably tried to 
            # get /people/17/ which returns a 404 for some reason.
            # Given more time, we'd also want to capture 5xx errors.
            logging.debug("Generating a new random number...")
            rando : int = generate_random_num()

            logging.debug("Getting people " + str(rando) + "...")
            get_people(rando)
    except Exception as e:
        logging.error("Something went wrong in the get_people function...")
        raise e

def save_people(people_id, name):
    try:
        insert_people = "INSERT INTO people (id, name) \
            VALUES ('" + str(people_id) + "','" + name + "')"
        db_cursor.execute(insert_people)
        db_cnx.commit()
    except Exception as e:
        logging.error("Something went wrong in the save_people function...")
        raise e

def save_people_in_films(people_id, film_id):
    try:
        insert_people_in_films = "INSERT INTO people_in_films (people_id, \
            film_id) VALUES ('" + str(people_id) + "','" + str(film_id) + "')"
        db_cursor.execute(insert_people_in_films)
        db_cnx.commit()
    except Exception as e:
        logging.error("Something went wrong in the save_people_in_films "
            "function...")
        raise e

def get_films():
    try:
        # Select distinct film ids from the database.
        db_cursor.execute("SELECT DISTINCT film_id FROM people_in_films")
        film_ids = db_cursor.fetchall()
        for (film_id,) in film_ids:
            logging.debug("Getting film " + str(film_id) + "...")

            # Assemble url.
            url : str = "https://swapi.co/api/films/" + str(film_id) + "/"

            # Hit the GET /films/ endpoint.
            response = requests.get(url)
            
            # Check if status_code is OK.
            if response.status_code == 200:
                data = response.json()
                title : str = data["title"]

                # Save films to films table.
                logging.debug("Saving film_id " + str(film_id) + ", " 
                    + title + " to the films table...")
                save_films(film_id, title)
            else:
                logging.debug("Film " + str(film_id) + " could not be found.")
                unknown_film_title : str = ("Film with id " +str(film_id) 
                    + " could not be retrieved ¯\\_(ツ)_/¯")
                save_films(film_id, "unknown_film_title")
    except Exception as e:
        logging.error("Something went wrong in the get_films function...")
        raise e

def save_films(film_id, title):
    try:
        insert_films = "INSERT INTO films (id, title) \
            VALUES ('" + str(film_id) + "','" + title + "')"
        db_cursor.execute(insert_films)
        db_cnx.commit()
    except Exception as e:
        logging.error("Something went wrong in the save_films function...")
        raise e

def main():
    try:
        logging.debug("Starting at " + str(datetime.datetime.now()) + "...")

        # Truncate tables so we can start fresh.
        logging.debug("Truncating tables...")
        tables : list = ["people","films","people_in_films"]
        for table in tables:
            truncate_sql : str = "TRUNCATE TABLE " + table
            db_cursor.execute(truncate_sql)

        # This is the number of people you want to return, 
        # parameterized in case you want to change it later.  Set at 
        # 15 per the requirements. Cannot be higher than 87 - we'd 
        # want to add an integrity check if this is parameterized down 
        # the road.
        desired_qty : int = 15

        # This is keeping track of the number of people we've retrieved 
        # from the SWAPI so far.
        ppl : int = count_ppl()

        while ppl < desired_qty:
            # Generate a random number and check if it has been used 
            # already.
            logging.debug("Generating random number...")
            rando : int = generate_random_num()

            # Get people (person) from the SWAPI.  Save them to the 
            # database along with their relationship to films.
            logging.debug("Getting people " + str(rando) + "...")
            get_people(rando)

            ppl = count_ppl()

        # Get films from the SWAPI.  Save them to the database.
        logging.debug("Getting films...")
        get_films()

        # Populate list.
        logging.debug("Populating list...")
        task_one_list : list = []

        # Iterate through films and add them to the list, along with 
        # their characters.
        db_cursor.execute("SELECT * FROM films")
        films = db_cursor.fetchall()
        for film in films:
            id : int = film[0]
            title: str = film[1]
            film_dict = {}
            logging.debug("Adding film " + title + " to list...")
            film_dict["film"] = title

            # Collect characters in film.
            db_cursor.execute("SELECT p.name FROM people_in_films pif \
                LEFT JOIN people p ON pif.people_id = p.id \
                WHERE pif.film_id = " + str(id))
            characters = db_cursor.fetchall()
            character_list : list = []
            for character in characters:
                name : str = character[0]
                logging.debug("Adding character " + name + " to film " 
                    + title + "...")
                character_list.append(name)

            film_dict["character"] = character_list
            task_one_list.append(film_dict)

        logging.debug("Printing list...")
        dump = json.dumps(task_one_list,indent=4)
        print(dump)

        db_cnx.close()

        logging.debug("Ending at " + str(datetime.datetime.now()) + ".")
    except Exception as e:
        logging.error("Something went wrong in the main function...")
        raise e

if __name__ == "__main__":
    main()