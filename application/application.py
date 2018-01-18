# 3rd party libraries
from flask import Flask, request, session, g
import json
import os
import pprint
from redis import Redis, StrictRedis
import sseclient
import time

# other imports
from celery_worker import make_celery

app = Flask('ScoreApplication') # create the application instance :)
app.config.from_object(__name__) # load config from this file , application.py
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = make_celery(app)
@celery.task
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
        if event.event == 'score':
            row = json.loads(event.data)
            students_score_cache.hset(row.get('studentId'), row.get('exam'), row.get('score'))
            exams_cache.hset(row.get('exam'), row.get('studentId'), row.get('score'))

            # log to celery workers
            print row

students_score_cache = StrictRedis(host='localhost', port=6379, db=1)
exams_cache = StrictRedis(host='localhost', port=6379, db=2)

@app.before_first_request
def before_first_request():
    fetch_data_from_content_server.delay()

@app.route('/ping', methods=['GET'])
def ping():
    """Test if server is alive"""
    return json.dumps({'hello': 'world'})

@app.route('/students', methods=['GET'])
def students():
    return json.dumps(students_score_cache.keys())

@app.route('/students/<name>', methods=['GET'])
def student_profile(name):
    return json.dumps(students_score_cache.hgetall(name))
