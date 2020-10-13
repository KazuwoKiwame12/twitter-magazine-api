from flask import Flask
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
def auth():
    return os.environ.get("BEARER_TOKEN")

def create_url(user_name):
    query ="from:"+user_name+" has:images"
    expansions_fields = "expansions=attachments.media_keys,author_id"
    media_fields = "media.fields=media_key,preview_image_url,type"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query,expansions_fields,media_fields
    )
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

@app.route('/search/tweets/<string:user_name>')
def search(user_name):
    bearer_token = auth()
    url = create_url(user_name)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json.dumps(json_response, indent=4)

@app.route('/')
def hello():
    return 'Hello world'