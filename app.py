from flask import Flask, render_template, jsonify
import requests
import json
import rsc
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Flask app
app = Flask(__name__)
rsc_client = rsc.Client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    data = rsc_client.invoke("queries/protectedObjects.gql")

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

