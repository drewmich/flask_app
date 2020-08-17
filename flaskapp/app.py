import json
from flask import Flask, render_template, redirect, url_for, request
import credentials
import requests
import startup
import base64
from logging import FileHandler, WARNING

app = Flask(__name__)
file_handler = FileHandler("errorlog.txt")
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)

#client credentials
CLIENT_ID = credentials.clientid
CLIENT_SECRET = credentials.clientsecret

#spotify links
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
CLIENT_SIDE_URL = "http://www.drewmi.ch"
PORT = 80
REDIRECT_URI = "http://www.drewmi.ch/callback"
SCOPE = "playlist-modify-private"
STATE = ""
HEADER = 'application/x-www-form-urlencoded'
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"


def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]


@app.route("/")
def home_function():
    return render_template("home.html")



@app.route("/spotify")
def spotify():
    return redirect("https://accounts.spotify.com/authorize?client_id=604f740a180c4f1f958bf7e166174f3e&response_type=code&redirect_uri=http%3A%2F%2Fwww.drewmi.ch%2Fcallback&scope=playlist-modify-private")




@app.route("/callback", methods=["POST", "GET"])
def callback():
    SPOT_CODE = request.args['code']
    
    body = {
        "grant_type": 'authorization_code',
        "code" : SPOT_CODE,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    #encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    #headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)}
    step_two = requests.post(TOKEN_ENDPOINT, data=body)

    #TOKEN_DATA = handleToken(json.loads(post.text)
    return render_template("redirect.html", variable=step_two.request.body)
#render_template("redirect.html")


@app.route("/projects")
def stuff_fxn():
    return render_template("construction.html")


