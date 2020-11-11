#!/bin/bash

. venv/bin/activate

export FLASK_APP=server.py

python data.py 60

deactivate