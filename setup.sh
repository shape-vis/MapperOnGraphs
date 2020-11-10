#!/bin/bash

# delete old directories
rm -rf __pycache__
rm -rf mog/__pycache__
rm -rf venv

# Create Virtual Environment
python3 -m venv venv

# Activate the environment
. venv/bin/activate

pip install --upgrade pip

#Within the activated environment, use the following command to install Flask and dependancies:
pip install wheel
#pip install Flask numpy python-dotenv watchdog simplejson blinker waitress gunicorn networkx scipy sklearn
pip install -r requirements.txt
pip freeze > requirements.txt

deactivate

