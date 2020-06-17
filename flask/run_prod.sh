#!/bin/bash

. venv/bin/activate

gunicorn -b 0.0.0.0:5000 main:app > run_prod.log 2>&1
