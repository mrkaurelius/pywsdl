#!/bin/bash
echo "BABAYAGA flask envvar setter"
.  /home/mrk0debian/pys/wsdl-flask/bin/activate
export FLASK_ENV=development
export FLASK_APP=flaskapp.py
printenv | grep -i flask
flask run
