#!/bin/bash

. venv/bin/activate

export FLASK_APP=main.py

flask run --host 0.0.0.0 --port 5000

