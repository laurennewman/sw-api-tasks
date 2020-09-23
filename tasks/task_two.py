import logging
import datetime
import requests
import json

logging.basicConfig(level=logging.DEBUG)


def get_data(id, resource):
    try:
        # Assemble url.
        url : str = "http://swapi.dev/api/" + resource + "/" + str(id) + "/"
        
        # Hit the GET /{resource}/ endpoint.
        response = requests.get(url)

        # Check if status_code is OK.
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 503:
            logging.debug("Resource " + url + " returned a status_code of " 
                + str(response.status_code) + ".")
            print("API service is unavailable.")
            quit()
        else:
            logging.debug("Resource " + url + " returned a status_code of " 
                + str(response.status_code) + ".")
    except Exception as e:
        logging.error("Something went wrong in the get_data function...")
        raise e


def list_nested_resources(dict):
    try:
        # Create a list of data elements that include urls.
        nested_resources : list = []
        for element in dict:
            # Skip url because it's a self-ref rather than a cross-ref.
            if element == "url" : continue

            if isinstance(dict[element], list):
                # This assumes that all lists are lists of urls, which 
                # they are *for now* but this could break if the API 
                # changes.
                nested_resources.append(element)
            elif isinstance(dict[element], str):
                if "http://swapi.dev/api/" in dict[element]:
                    nested_resources.append(element)
        logging.debug("Nested resources are " + str(nested_resources))
        return nested_resources
    except Exception as e:
        logging.error("Something went wrong in the list_nested_resources "
            "function...")
        raise e


def get_nested_resources(dict, nested_resources):
    try:
        # Iterate through nested resources lists.
        for resource in nested_resources:
            resource_list : list = dict[resource]
            new_resource_list : list = []

            # Annoying override of "characters" to "people".
            if resource == "characters": resource = "people"
            
            # Assemble base url.
            base_url = "http://swapi.dev/api/" + resource + "/"
            
            # Get nested data from the SWAPI.
            for item in resource_list:
                id : int = (item[len(base_url):len(item)-1])
                logging.debug("Getting nested resource " + base_url 
                    + str(id) + "/...")
                data = get_data(id, resource)
                
                # Strip cross-referencing material from nested data.
                cross_refs : list = list_nested_resources(data)
                for cross_ref in cross_refs:
                    logging.debug("Popping " + cross_ref 
                        + " cross-refs from " + resource + "...")
                    data.pop(cross_ref)

                new_resource_list.append(data)

            logging.debug("Replacing list of " + resource 
                + " urls with data...")
            if resource == "people": resource = "characters"
            dict[resource] = new_resource_list
    except Exception as e:
        logging.error("Something went wrong in the "
            "get_nested_resources function...")
        raise e


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def convert_character_units(dict):
    try:
        for character in dict["characters"]:
            # Strip commas because some characters are fatties with 
            # weights  exceeding 1,000 kilograms.
            stripped_height : str = character["height"].replace(",","")
            stripped_mass : str = character["mass"].replace(",","")

            # Convert height from centimeters to feet and inches.
            if is_number(stripped_height):
                metric_height : float = float(stripped_height)
                
                height_total_inches : float = metric_height / 2.54
                height_feet : int = int(height_total_inches // 12)
                height_inches : int = (round(height_total_inches 
                    - (height_feet * 12)))

                standard_height : str = (str(height_feet) + " feet " 
                    + str(height_inches) + " inches")
                
                logging.debug("Converted " + str(metric_height) 
                    + " centimeters to " + standard_height + ".")
                character["height"] = standard_height

            # Convert mass from kilograms to pounds.
            if is_number(stripped_mass):
                metric_mass : float = float(stripped_mass)

                mass_pounds : float = round(metric_mass * 2.205)
                
                standard_mass : str = str(mass_pounds) + " pounds"
                
                logging.debug("Converted " + str(metric_mass) 
                    + " kilograms to " + standard_mass + ".")
                character["mass"] = standard_mass
    except Exception as e:
        logging.error("Something went wrong in the convert_units "
            "function...")
        raise e


def main():
    try:
        logging.debug("Starting at " + str(datetime.datetime.now()) + "...")

        # Set the film_id for A New Hope, or whatever film you want. 
        # Cannot be greater than 7.
        film_id : int = 1

        # Get film from the SWAPI.
        logging.debug("Getting film " + str(film_id) + "...")
        film = get_data(film_id, "films")

        # Get film's characters, planets, species, starships, and 
        # vehicles from the SWAPI
        logging.debug("Getting nested resources...")
        nested_resources: list = list_nested_resources(film)
        get_nested_resources(film, nested_resources)

        # Convert metric height and mass to standard units.
        logging.debug("Converting units of measurement...")
        convert_character_units(film)

        # Assemble json file.
        logging.debug("Writing list to file...")
        dump = json.dumps(film,indent=4)

        file = open("task_two.json", "w")
        file.write(dump)
        
        logging.debug("Ending at " + str(datetime.datetime.now()) + ".")
    except Exception as e:
        logging.error("Something went wrong in the main function...")
        raise e


if __name__ == "__main__":
    main()
