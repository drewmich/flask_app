from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "604f740a180c4f1f958bf7e166174f3e"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "2b6aaa9aa91f4355b5879257301dab48"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "80"
CALLBACK_URL = "http://www.drewmi.ch/redirect"

#Add needed scope from spotify user
SCOPE = "playlist-modify-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
