import json
from flask import Flask, render_template, redirect, url_for, request
import credentials
import requests
import startup
import base64
from logging import FileHandler, WARNING
import urllib.parse

app = Flask(__name__)
file_handler = FileHandler("errorlog.txt")
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)


   ##############################
   ###                        ###
   ###   Utility Variables    ###
   ###                        ###
   ##############################

CLIENT_ID = credentials.clientid
CLIENT_SECRET = credentials.clientsecret
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

#Homepage function
@app.route("/")
def home_function():
    return render_template("home.html")


#Immediately redirects users to spotify login page for web app
#Follows Spotify's "Authorization Code Flow"
@app.route("/spotify")
def spotify():
    return redirect("https://accounts.spotify.com/authorize?client_id=604f740a180c4f1f958bf7e166174f3e&response_type=code&redirect_uri=http%3A%2F%2Fwww.drewmi.ch%2Fcallback&scope=playlist-modify-private")



@app.route("/callback", methods=["POST", "GET"])
def callback():

    #Recieves login callback from spotify, parses for authorization code
    SPOT_CODE = request.args['code']
    
    body = {
        "grant_type": 'authorization_code',
        "code" : SPOT_CODE,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    #Makes call to spotify to exchange authorization code for access token
    step_two = requests.post(TOKEN_ENDPOINT, data=body)
    new_data = json.loads(step_two.text)
    TOKEN = new_data['access_token']

    #Page where users customize their playlist
    return render_template("playlist.html", user_token_ = TOKEN)

@app.route("/playlist", methods=["POST", "GET"])
def playlist():

    #Sets variables with data from submitted form
    name = request.form['playlist_name']
    bpm = request.form['bpm']
    popularity = request.form['popularity']
    numberSongs = request.form['songs']
    genre = request.form['genre']
    seed_genres = genre
    tempo = bpm
    limit = numberSongs
    TOKEN = request.form['usr_token']

    #Sets Authorization Header for future requests
    HEADER = { "Authorization" : "Bearer {}".format(TOKEN) } 

    
    #Gets user_id for use in API calls
    user_data = requests.get("https://api.spotify.com/v1/me", headers=HEADER)
    user_data_text = json.loads(user_data.text)
    userID = user_data_text['id']


    #Setup for making empty playlist to be filled
    #Returns a playlist object
    playlistCallURL = "https://api.spotify.com/v1/users/{}/playlists".format(userID)
    contentType = "application/json"
    BODY_PLAYLIST = {

        "name" : name,
        "description" : "Runify playlist for {}".format(userID),
        "public" : False
        
    }

    jsonBody = json.dumps(BODY_PLAYLIST)

    HEADER_ADD = { "Authorization" : "Bearer {tkn}".format(tkn=TOKEN), "Content-Type" : "application/json" }

    #Call to make empty playlist
    playlist_data = requests.post(playlistCallURL, headers=HEADER_ADD, data=jsonBody)
    playlist_data_text = json.loads(playlist_data.text)
    playlistID = playlist_data_text['id']


    #Body for Get Recommendations call
    BODY_REC = {
        "seed_genres" : genre,
        "tempo" : bpm,
        "limit" : numberSongs,
        "popularity" : popularity
    }

    rec_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(TOKEN)
    }

    rec_params = (
    ('limit', limit),
    ('seed_genres', seed_genres),
    ('target_popularity', popularity),
    ('target_tempo', tempo),
    )
    
    rec_url = urllib.parse.urlencode(BODY_REC)
    final_url = "https://api.spotify.com/v1/recommendations?" + rec_url 

    #Makes call to spotify
    #This is where the songs that fit user criteria are fetched
    recommendations_data = requests.get(final_url, headers=rec_headers)

    recommendations_data_text = json.loads(recommendations_data.text)

    
    #Grabs the array of track objects returned by spotify that fit user input
    tracksArray = recommendations_data_text['tracks'] 

    trackUriList = []

    trackString = ""

    #Iterates through tracks array, and adds necessary text to a list of 
    #strings that will be sent to spotify to add tracks to the user's empty playlist
    for item in tracksArray:

        trackString =  item['uri']
        trackUriList.append(trackString)

    urisList = {"uris" : trackUriList }

    jsonUrisList = json.dumps(urisList)

    add_songs_url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistID)

    #Request to add tracks to the user's playlist
    add_data = requests.post(add_songs_url, headers=HEADER_ADD, data=jsonUrisList)
    
    add_data_text = json.loads(add_data.text)


    return render_template("success.html")
        


@app.route("/projects")
def stuff_fxn():
    return render_template("construction.html")
