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

    step_two = requests.post(TOKEN_ENDPOINT, data=body)
    new_data = json.loads(step_two.text)
    TOKEN = new_data['access_token']
    


    return """
        <html>
        <head>
        </head>
        <body>
             <h2> Let's make your playlist</h2>
             <form action="/playlist">
                 Playlist name <input type='text' name='playlist_name'><br>
                 Genre <input type='text' list="genres" name="genre"><br>
 
                <input type="hidden" name="usr_token" value={}>

                <datalist id="genres">
                   <option value="alternative"/>
                   <option value="chill"/>
                   <option value="club"/>
                   <option value="country"/>
                   <option value="dance"/>
                   <option value="death-metal"/>
                   <option value="deep-house"/>
                   <option value="edm"/>
                   <option value="hard-rock"/>
                   <option value="hip-hop"/>
                   <option value="house"/>
                   <option value="indie"/>
                   <option value="metal"/>
                   <option value="party"/>
                   <option value="pop"/>
                   <option value="rock"/>
                 </datalist>

                 BPM <input type="text" list="bpm" name="bpm"><br>

                <datalist id="bpm">
                   <option value="130"/>
                   <option value="135"/>
                   <option value="140"/>
                   <option value="145"/>
                   <option value="150"/>
                   <option value="155"/>
                   <option value="160"/>
                   <option value="165"/>
                   <option value="170"/>
                   <option value="175"/>
                   <option value="180"/>
                   <option value="185"/>
                   <option value="190"/>
                </datalist>

                Number of Songs <input type="text" list="songs" name="songs"><br>
<datalist id="songs">

               <datalist id="songs">
                  <option value="5"/>
                  <option value="6"/>
                  <option value="7"/>
                  <option value="8"/>
                  <option value="9"/>
                  <option value="10"/>
                  <option value="11"/>
                  <option value="12"/>
                  <option value="13"/>
                  <option value="14""/>
                  <option value="15"/>
                  <option value="16"/>
                  <option value="17"/>
                  <option value="18"/>
                  <option value="19"/>
                  <option value="20"/>
                  <option value="21"/>
                  <option value="22"/>
                  <option value="23"/>
                  <option value="24"/>
                  <option value="25"/>

               </datalist>
                
                Popularity 0-100 (optional) <input type='text' name='popularity'><br>

                 <input type='submit' value='Continue'>
             </form>
            
             
         </body>
         </html>
         """.format(TOKEN)

@app.route("/playlist", methods=["POST", "GET"])
def playlist():

    #Sets variables with data from submitted form
    name = request.args.get('playlist_name')
    bpm = request.args.get('bpm')
    popularity = request.args.get('popularity')
    numberSongs = request.args.get('songs')
    genre = request.args.get('genre')
    seed_genres = genre
    tempo = bpm
    limit = numberSongs
    TOKEN = request.args.get('usr_token')

    #Sets Authorization Header for function
    HEADER = { "Authorization" : "Bearer {}".format(TOKEN) } 

    
    #Gets user_id for use in API calls
    user_data = requests.get("https://api.spotify.com/v1/me", headers=HEADER)
    user_data_text = json.loads(user_data.text)
    userID = user_data_text['id']


    #Makes playlist to be filled
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

    playlist_data = requests.post(playlistCallURL, headers=HEADER_ADD, data=jsonBody)
    playlist_data_text = json.loads(playlist_data.text)
    #return playlist_data_text
    
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

    #response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)

    #Call
    #recommendations_data = requests.get("https://api.spotify.com/v1/recommendations", headers=rec_headers, params=rec_params)
    
    rec_url = urllib.parse.urlencode(BODY_REC)
    final_url = "https://api.spotify.com/v1/recommendations?" + rec_url 

    recommendations_data = requests.get(final_url, headers=rec_headers)

    recommendations_data_text = json.loads(recommendations_data.text)

    #returnvaltest = final_url+seed_genres+bpm+limit+popularity

    tracksArray = recommendations_data_text['tracks'] 

    trackUriList = []

    trackString = ""

    
    for item in tracksArray:

        trackString =  item['uri']
        trackUriList.append(trackString)

    urisList = {"uris" : trackUriList }

    jsonUrisList = json.dumps(urisList)

    add_songs_url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistID)

    add_data = requests.post(add_songs_url, headers=HEADER_ADD, data=jsonUrisList)
    
    add_data_text = json.loads(add_data.text)



    return "Success!"
        


@app.route("/projects")
def stuff_fxn():
    return render_template("construction.html")
