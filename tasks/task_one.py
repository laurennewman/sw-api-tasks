import datetime
import logging
from os import environ

from helpers.api_helpers import get_character, get_films
from helpers.db_helpers import connect_to_mysql, create_database, count_characters
from helpers.util_helpers import generate_unique_random_number, format_and_print_results

logging.basicConfig(level=environ["LOG_LEVEL"])


def main():
    try:
        logging.debug(f"Starting task one at {datetime.datetime.now()}")

        db_cnx, db_cursor = connect_to_mysql()

        create_database(db_cursor)

        random_numbers = []

        while count_characters(db_cursor) < 15:
            random_number, random_numbers = generate_unique_random_number(random_numbers)
            get_character(db_cursor, random_number)

        get_films(db_cursor)

        format_and_print_results(db_cursor)

        db_cnx.close()

        logging.debug(f"Finished task one at {datetime.datetime.now()}")
    except Exception as e:
        logging.error(f"Something went wrong: {e}")
        raise


if __name__ == "__main__":
    main()
