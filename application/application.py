# all the imports
import json
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask('ScoreApplication') # create the application instance :)
app.config.from_object(__name__) # load config from this file , application.py

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/students', methods=['GET'])
def students():
    return json.dumps({'hello': 'world'})
