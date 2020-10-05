# Ethitical AI Platform

# Todo:

- Create workflow
- Discuss front-end choices
- Start migrating the code to this project

# Installation

Since custom package and specific package version are used in this project, we recommend using `venv` for development so your local python env won't be polluted.

**If you intended to install on global field, please ignore `venv` part**

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