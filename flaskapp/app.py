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



@app.route("/")
def home_function():
    return render_template("home.html")



@app.route("/spotify")
def spotify():
    return redirect("https://accounts.spotify.com/authorize?client_id=604f740a180c4f1f958bf7e166174f3e&response_type=code&redirect_uri=http%3A%2F%2Fwww.drewmi.ch%2Fcallback&scope=playlist-modify-private")




@app.route("/callback")
def callback():
    startup.getUserToken(request.args['code'])
    return render_template("redirect.html")


@app.route("/projects")
def stuff_fxn():
    return render_template("construction.html")

