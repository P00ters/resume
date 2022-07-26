#!/bin/bash
sudo apt-get install python3 python3-pip
python3 -m pip install virtualenv
python3 -m virtualenv venv
chmod +x venv/bin/activate
source venv/bin/activate
python3 -m pip install flask
python -m pip install Flask-Mobility
python -m pip install -U flask_cors
deactivate
