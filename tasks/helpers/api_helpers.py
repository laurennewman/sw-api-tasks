import logging
from os import environ

import requests

from helpers.db_helpers import insert_character, insert_characters_in_films, select_film_ids, insert_film

logging.basicConfig(level=environ["LOG_LEVEL"])


def make_get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e.response.text}")
        return e.response
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error connecting: {e.response.text}")
        raise e
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout error: {e.response.text}")
        raise e
    except requests.exceptions.RequestException as e:
        logging.error(f"Something went wrong: {e.response.text}")
        raise e


def get_character(db_cursor, character_id):
    logging.info(f"Getting character id {character_id}")
    url = f"{environ['BASE_API_URL']}people/{character_id}/"
    response = make_get_request(url)

    if response.status_code == 200:
        character = response.json()
        name = character["name"]
        insert_character(db_cursor, character_id, name)

        films = character["films"]
        for film in films:
            film_id = (film[len(f"{environ['BASE_API_URL']}films/"): len(film) - 1])
            insert_characters_in_films(db_cursor, character_id, film_id)


def get_films(db_cursor):
    film_ids = select_film_ids(db_cursor)

    for (film_id,) in film_ids:
        logging.info(f"Getting film id {film_id}")
        url = f"{environ['BASE_API_URL']}films/{film_id}/"
        response = make_get_request(url)

        if response.status_code == 200:
            film = response.json()
            title = film["title"]
            insert_film(db_cursor, film_id, title)
