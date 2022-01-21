#!/bin/bash


if [ "$1" = "clean" ]
then
  # delete old directories
  rm -rf __pycache__
  rm -rf venv
fi

if [ -d "venv/" ]
then
  # Activate the environment
  . venv/bin/activate
else
  # Create Virtual Environment
  python3 -m venv venv

  # Activate the environment
  . venv/bin/activate

  pip install --upgrade pip

  #Within the activated environment, use the following command to install Flask and dependancies:
  pip install wheel flask
  #pip install Flask numpy python-dotenv watchdog simplejson blinker waitress gunicorn networkx scipy sklearn
  pip install -r requirements.txt
  pip freeze > requirements.txt
fi


#python data.py 0
python data.py 1
#python data.py 30
python data.py 900

deactivate
