# Project Amazon Data Base

Welcome to our project trying to replicate one of the most common e-commerce shopping sites Amazon in this project we developed two databases in postgres and sql making use of WebServices in python along with some imports such as FastAPI MySQL Connection among others.

##Introduction
Currently this project includes with:
- **Web Services:** Web services in a wide variety of tables as follows
- **Database Connections:** Connection to SQL and Postgres databases

## Database Design

Our database design was done with the purpose of trying to abstract as much information as possible about what an amazon database supports in the e-commerce aspect as you will see below in this diagram

![Definitive drawio](https://github.com/user-attachments/assets/8c7eaf2f-c5ae-45cd-8129-aa3a07d19e38)

## How to Use

Its use is very simple since Uvicorn makes it easier to execute everything without so much complication.

### Step 1: Database initialization

First, we start our database with docker compose using the command:
```bash
docker-compose up -d
```
Make sure you are correctly located in the project, otherwise it will not load the required service.

### Step 2: Checking the database

In the terminal after having started the docker compose we have to check the connection we execute the following command to know if both Postgres and MySQL are working correctly
```bash
python PGDatabase_Connection.py
```
```bash
python SQLDatabase_Connection.py
```
After this the terminal will check if there really is a successful connection or not. 

### Step 3: Running the code

once this is done we directly execute the following code and wait for it to load completely 

``` bash
python -m uvicorn main:app --reload
```

after this we open our localhost in a browser page using the following link 

```bash
http://localhost:8000/docs#/
```

Finally everything will be complete and you will be able to make use of this database by creating, updating and deleting as you wish.

## Technology Stack:

- __Backend__: FastAPI framework.
- __Databases__: MySQL and PostgreSQL.
- __Containerization__: Docker and Docker Compose.

I hope this program will be useful for your research or studies and I will see you another time.
