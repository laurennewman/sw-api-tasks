import json
import logging
import random
from os import environ

from helpers.db_helpers import select_films, select_characters_in_films

logging.basicConfig(level=environ["LOG_LEVEL"])


def generate_unique_random_number(random_numbers):
    is_unique = False

    while not is_unique:
        random_number = random.randint(1, 87)
        logging.debug(f"Generated random number {random_number}")
        is_unique = check_uniqueness(random_number, random_numbers)

    random_numbers.append(random_number)

    return random_number, random_numbers


def check_uniqueness(random_number, random_numbers):
    if random_number in random_numbers:
        logging.debug(f"Random number {random_number} is not unique")
        return False

    return True


def format_and_print_results(db_cursor):
    output = []

    for film in select_films(db_cursor):
        add_characters_to_film(db_cursor, film, output)

    print(json.dumps(output, indent=4))


def add_characters_to_film(db_cursor, film, output):
    film_id = film[0]
    title = film[1]

    logging.debug(f"Adding film {title} to list")
    film_dict = {"film": title}

    character_list = []

    characters = select_characters_in_films(db_cursor, film_id)

    for character in characters:
        name = character[0]
        logging.debug(f"Adding character {name} to film {title}")
        character_list.append(name)

    film_dict["character"] = character_list

    output.append(film_dict)
