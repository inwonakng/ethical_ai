# Ethical AI Platform

# Development setup
- migrate the latest model changes to the database by running the following commands

```bash
python manage.py makemigrations
python manage.py migrate
``` 
- If you run in to errors, either go in the docker shell or command line and run the following query to reset the database

```sql
DROP DATABASE mysqldb; CREATE DATABASE mysqldb;
```

- After you migrate, create a user in the database by running the app and going to \register
- Once you create a user, run the django shell in order to populate the database

```bash
python manage.py shell
```

- Then copy and run the code in defulat_database.py in the repo's root folder
- Now you should have the current setup for testing.


# Installation

Since custom package and specific package version are used in this project, we recommend using `venv` for development so your local python env won't be polluted.

## Configure MySQL

### Using Docker

#### Starting MySQL and PHPMyAdmin

```bash
docker-compose -f docker-compose.dev.yml up -d
```

This command will run a latest mysql w/ combination `root/password` on `127.0.0.1:3306` and phpmyadmin on `127.0.0.1:8088`. You may use this web interface to manage the database.

#### Remove/Recreate Mysql

```bash
docker-compose -f docker-compose.dev.yml down
```

And recreate using the first command.

## Manually installing and setting up MySQL

linux:

```
sudo apt install mysql-server
```

If you install the server any other way and are prompted with a password, leave the field blank.
If you set the password, you may not need to do the step below.

### Fixing privilege

After running MySQL with admin priveges (sudo), run the following queries to reset the root password.

```
DROP USER 'root'@'localhost';
CREATE USER 'root'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE mysqldb
```

### Hotfix to run db with django 2.2

`python3 -m site`
to find your site packages directory

Then go locate the file in django directory
`django/db/backends/mysql/operations.py`

Find the line with `query = query.decode(errors='replace')`

Remove the line and put `query = errors='replace'`

### If you intended to install on global field, please ignore `venv` part

## venv

```bash
python3 -m venv venv
```

The above command will generate `venv` under current directory

### Enter Virtualenv

```bash
source venv/bin/activate
```

You should now see `(venv)` in front of your command ine

### Exit Virtualenv

```bash
deactivate
```

## Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Add new dependency

After adding new dependency, run the following command to lock requirements.txt

```bash
pip freeze > requirements.txt
```

<!--@TODO if custom packages uses, we could have a script to move then into `venv` or let user do their global package stuff.-->

## Configuring typescript

### Download npm

if you do not have npm downloaded already, use `sudo apt install npm` to install npm.

### Install typescript

use this command to then install typescript `sudo npm install -g typescript`

### Install library for typescript

use this command to make the node.js library to be available to typescript `npm install -D @types/node`

## Migration & Start Server

```bash
cd ethicssite
python3 manage.py migrate
python3 manage.py createcachetable
```

and start server by

```bash
python3 manage.py runserver
```


## Compiling the typescript files 
**make sure the change the relative path if you are not executing from the root directory
```bash
tsc -p ethicssite/static/scripts/tsconfig.json
```