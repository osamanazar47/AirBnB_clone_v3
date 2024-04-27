#!/usr/bin/python3
"""
Starts flask web application
- my first endpoint (route) will be to return
the status of your API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    flask_run_host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    flask_run_port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=flask_run_host, port=flask_run_port, threaded=True)

