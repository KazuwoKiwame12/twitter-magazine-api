from flask import Flask
import os
import requests
import json
import datetime

# from dotenv import load_dotenv

# load_dotenv()
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def auth():
    return os.environ.get("BEARER_TOKEN")

def create_url(user_name):
    query ="from:"+user_name+" has:images"
    tweet_fields = "tweet.fields=created_at"
    expansions_fields = "expansions=attachments.media_keys,author_id"
    media_fields = "media.fields=media_key,url"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query,tweet_fields,expansions_fields,media_fields
    )
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    results = requests.request("GET", url, headers=headers)
    if results.status_code != 200:
        raise Exception(results.status_code, results.text)
    results_json = results.json()
    print(results_json)
    return change_to_client_format(results_json)

def change_to_client_format(search_result):
    user_name = search_result["includes"]["users"][0]["name"]
    media = search_result["includes"]["media"]

    tweets_for_client = []
    for tweet in search_result["data"]:
        tweet_for_client = {
            "author": user_name,
            "checked": False,
            "created_at": tweet["created_at"],
            "text": tweet["text"],
            "images": get_images_from_keys(tweet["attachments"]["media_keys"], media)
        }
        tweets_for_client.append(tweet_for_client)
    return tweets_for_client

def get_images_from_keys(media_keys, media):
    images = [val["url"] for val in media if media_keys.count(val["media_key"])]
    return images

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
