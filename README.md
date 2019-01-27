# swapi-tasks

## Requirements Doc
see [Red Hat Technical Assessment - Data Engineer.pdf](Red%20Hat%20Technical%20Assessment%20-%20Data%20Engineer.pdf)

## Pre-reqs
* Python 3.x
* MySQL
* Requests library
* MySQL Connector/Python

```
pip install requests
pip install mysql-connector-python
```

## Instructions
### Task 1
1. Enter and save your database credentials at the top of create_database.py
2. Execute create_database.py to create a database named "swapi_tasks" with the required tables
3. Enter and save your database credentials at the top of task_one.py
4. Execute task_one.py and confirm results in the console

### Task 2
1. Execute task_two.py and confirm results in the json file

## Database schema
### people
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int(11) | NO | PRI | NULL |  |
| name | varchar(255) | NO |  | NULL |  |

### films
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int(11) | NO | PRI | NULL |  |
| title | varchar(255) | NO |  | NULL |  |

### people_in_films
| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| people_id | int(11) | NO |  | NULL |  |
| film_id | int(11) | NO |  | NULL |  |