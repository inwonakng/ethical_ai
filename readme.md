# Spring Semester TODO:
### Convert the app to frontend/backend separate!
- After some tries with the views, I came to the conclusion that it would be easier to turn the django backend to provide the json for the javascript frontend to consume.
- learning from last semester, we will discuss this early on, and make a decision and stick to it.
- already the django template is getting messy, and our application needs to be able to display more complex analysis screens in the future, which will result in a lot of bloated code.
- We can do this parellely, if anyone wants to take a crack at setting up a react/vue frontend application.
## Pages to finish:
- My survey
- My taken survey
- Survey Review page at the end



# CODING STYLE GUIDE
### Overall
- Some parts were written in a rush, so they are misssing documentation. If you encounter any such method, try to write a simple comment on top. If unclear, please contact Inwon. We should strive to have all the methods commented at the end of the semester.

### Backend
- Every time you write a query, explain what the conditions are explicitly
- Try to avoid redundant loops, use pythonic code if possible (list comprehension, negative indexing, etc...)

### Frontend (Django template)
- We should strive to have as little js as possible in the frontend when using django templates.
- If necessary we use jquery, BUT please explicitly document what the function is doing.
- more concise/modular code is better. If you have to copy and paste a function, think about where that code should be placed so that you can avoid that. 
- (almost) Everything should use flex! if you do not know how to use this, look up flex, flex-direction, display:flex. If you encounter examples of html elements breaking because of fixed length (width:XXXpx and such) please take the time to convert everything to flex. Using flex will help us have everything modular and scale accordingly to different screen sizes.

### Refactoring
- Anytime you find a piece of css or file that is never called (good way to check is ctrl+shift+F in vscode to search entire project), please remove it. Obviously don't do this if you are not sure. However if it doesn't appear anywhere on the project search, it is safe to remove.



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
DROP USER 'root'@'%';
CREATE USER 'root'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE mysqldb
```

## venv 
### You should always use venv! This will help us isolate the dependencies of our project to make for easier installation

```bash
python3 -m venv venv
```

The above command will generate `venv` under current directory

### Enter Virtualenv

```bash
source venv/bin/activate
```

```cmd.exe
<venv>\Scripts\activate.bat
```

```PowerShell
<venv>\Scripts\Activate.ps1
```

#### On windows, try to stick to powershell, which is the default vscode terminal.

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
