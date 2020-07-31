import json
from flask import Flask, render_template, redirect, url_for, request
import credentials
import requests
import startup
import base64
from urllib import quote, urlencode

app = Flask(__name__)

#client credentials
CLIENT_ID = credentials.clientid
CLIENT_SECRET = credentials.clientsecret

#spotify links
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
CLIENT_SIDE_URL = "http://www.drewmi.ch"
PORT = 80
REDIRECT_URI = "http://www.drewmi.ch/redirect"
SCOPE = "playlist-modify-private"
STATE = ""



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
    #return redirect(f"{SPOTIFY_AUTH_URL}/?{urllib.parse.urlencode(payload)}")
    return redirect("https://accounts.spotify.com/authorize?client_id=604f740a180c4f1f958bf7e166174f3e&response_type=code&redirect_uri=http%3A%2F%2Fwww.drewmi.ch%2Fredirect&scope=playlist-modify-private")


    # response = startup.getUser()
    # return redirect(response)



@app.route("/redirect")
def redirect():
    startup.getUserToken(request.args['code'])
    return render_template("redirect.html")
