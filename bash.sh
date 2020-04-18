#!/bin/bash
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
source .envrc
python ./manage.py migrate
#python ./manage.py loaddata datalabApp/fixtures/quickstart.json
python ./manage.py runserver
python ./manage.py test
