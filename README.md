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
After the docker container is up and running ensure .env fits your needs change the database accordingly to the db created in the previous step.

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

## Docker
This app can also be build and run with docker containers. It uses docker and docker-compose which expect a .env file (which is the same as the roche_back/.env_example). 

First, Docker must be installed:

* Windows: https://docs.docker.com/desktop/windows/install/
* Ubuntu: https://docs.docker.com/engine/install/ubuntu/
* Mac: https://docs.docker.com/desktop/mac/install/

After installing Docker Desktop, on Windows and Mac there is no need to install _docker-compose_, for Linux follow instructions on the https://docs.docker.com/compose/install/.



To build and run simply do (if you don't want to build, just ommit the `--build`):
```shell script
 docker-compose --env-file roche_back/.env up --build -d 
 ```

### Inital provisioning
As described above the app requires you to initially run migrations, docker equivalents of those are bellow:
```shell script
docker exec -it roche-back_backend_1 python manage.py makemigrations
docker exec -it roche-back_backend_1 python manage.py migrate
```
### Empty and repopulate DB with example data
```shell script
docker exec -it roche-back_backend_1 python manage.py db_seed --force True
```
