#!/bin/bash
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
source .envrc
python ./manage.py migrate
python ./manage.py test
python ./manage.py runserver
