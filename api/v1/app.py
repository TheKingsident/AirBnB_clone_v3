#!/usr/bin/python3
"""API to return status"""
from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
