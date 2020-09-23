# swapi-tasks

## How to run
### Task 1
1. Create and activate a virtual environment
2. Install required libraries with `pip install -r requirements.txt`
3. Enter and save your database credentials in `run_task_one.sh`
4. Execute `run_task_one.sh` and confirm the results in the console output

### Task 2
1. Simply execute `run_task_two.sh` and confirm results in the json file

## Database schema
### characters
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int(11) | NO | PRI | NULL |  |
| name | varchar(255) | NO |  | NULL |  |

### films
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int(11) | NO | PRI | NULL |  |
| title | varchar(255) | NO |  | NULL |  |

### characters_in_films
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| character_id | int(11) | NO |  | NULL |  |
| film_id | int(11) | NO |  | NULL |  |