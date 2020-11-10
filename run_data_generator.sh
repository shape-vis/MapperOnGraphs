#!/bin/bash

. venv/bin/activate

export FLASK_APP=server.py

python data.py 1

deactivate