# RocheHackaton 2021: Team GasterByteri
##### Authors: 

Table of contents:
1. [Setup](#setup)

<a name="setup"></a>
## Setup
1. In order to install all the project related dependencies issue:
```shell script

git clone https://github.com/GasterByteri/roche-back.git && cd roche-back
pip install -r requirements.txt  
```

2. Postgres database is localhosted and run as a docker container. In order to setup database run:

```shell script
docker run -d --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=roche_db -p 5432:5432 postgres:13
```
After the docker container is up and running rename the .env_example to .env and change the database accordingly to the db created in the previous step.

3. After the db is up and running, issue following commands to create migrations:
```shell script
cd <repo_root>
python manage.py makemigrations
python manage.py migrate
```
4. To start the application run django server with the following command:
```shell script
python manage.py runserver
```
5. After the server is up and running the welcome endpoint is exposed at url `http://127.0.0.1:8000/api/welcome`. 
6. To pre-populate database with test data issue:
```bash
python manage.py db_seed --force True
```