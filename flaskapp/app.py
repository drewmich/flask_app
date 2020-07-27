import json
from flask import Flask, render_template, redirect, url_for, request
import credentials
import requests
import startup
from urllib.parse import quote


app = Flask(__name__)

#client credentials
CLIENT_ID = credentials.clientid
CLIENT_SECRET = credentials.clientsecret

#spotify links
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
# SPOTIFY_API_BASE_URL = "https://api.spotify.com"
# API_VERSION = "v1"
# SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
# SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
#
# #More
CLIENT_SIDE_URL = "http://www.drewmi.ch"
PORT = 80
REDIRECT_URI = "{}:{}/redirect".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-private"
STATE = ""
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
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state' : STATE,
        'scope': SCOPE,
    }

    res = make_response(redirect(f'{SPOTIFY_AUTH_URL}/?{urlencode(payload)}'))
    return res
    # response = startup.getUser()
    # return redirect(response)



@app.route("/redirect")
def redirect():
    startup.getUserToken(request.args['code'])
    return render_template("redirect.html")
