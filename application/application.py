# all the imports

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import json
import os
import pprint
import sseclient

app = Flask('ScoreApplication') # create the application instance :)
app.config.from_object(__name__) # load config from this file , application.py

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/students', methods=['GET'])
def ping():
    """Test if server is alive"""
    return json.dumps({'hello': 'world'})

@app.before_first_request
def fetch_data_from_content_server():
    #0. connect to content server and load its data to memory
    def with_requests(url):
        """Get a streaming response using requests library."""
        import requests
        return requests.get(url, stream=True)

    content_server_url = "http://live-test-scores.herokuapp.com/scores"
    response = with_requests(content_server_url)
    client = sseclient.SSEClient(response)
    for event in client.events():
        print json.loads(event.data)
