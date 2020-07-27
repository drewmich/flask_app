import json
from flask import Flask, render_template, redirect, url_for, request
import credentials
import requests
import startup
from urllib.parse import quote


app = Flask(__name__)

#client credentials
# CLIENT_ID = credentials.clientid
# CLIENT_SECRET = credentials.clientsecret

#spotify links
# SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
# SPOTIFY_API_BASE_URL = "https://api.spotify.com"
# API_VERSION = "v1"
# SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
# SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
#
# #More
# CLIENT_SIDE_URL = "http://www.drewmi.ch/spotify"
# PORT = 8000
# REDIRECT_URI = "{}:{}/redirect".format(CLIENT_SIDE_URL, PORT)
# SCOPE = "playlist-modify-private"
# STATE = ""
# SHOW_DIALOG = "false"
#
# auth_query_parameters = {
#     "response_type": "code",
#     "redirect_uri": REDIRECT_URI,
#     "scope": SCOPE,
#     # "state": STATE,
#     # "show_dialog": SHOW_DIALOG_str,
#     "client_id": CLIENT_ID
# }


@app.route("/")
def home_function():
    return render_template("home.html")



@app.route("/spotify")
def spotify():
    response = startup.getUser()
    return redirect(response)
    # url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    # auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    # return redirect(auth_url)


@app.route("/redirect")
    startup.getUserToken(request.args['code'])

    # #Authorization 2nd call
    # auth_token = request.args['code']
    # code_payload = {
    #     "grant_type": "authorization_code",
    #     "code": str(auth_token),
    #     "redirect_uri": REDIRECT_URI,
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET,
    # }
    # post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    #
    # #Returns from 2nd call
    # response_data = json.loads(post_request.text)
    # access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]
    #
    # #Use access token to access spotify API on user behalf
    # authorization_header = {"Authorization": "Bearer {}".format(access_token)}
