
# This is the code for my AWS based EC2 instance for my website.

## Spotify web app to create custom playlists on your profile

*Pictures at bottom*

Hosted on this website is my spotify web app to create custom playlists on a user's profile. The purpose of this app is to give Spotify listeners access to the customization that the Spotify's Web API allows, without actually having to code anything. Users can select genre, beats per minute, number of songs, popularity of songs, and popularity of the songs. The original goal was to create playlists for going on runs, but it can be used for making playlists for anything.

When users land on my website, clicking the link called "Spotify App" will automatically redirect first time users to the spotify login page. The app uses Spotofy's Authorization code Flow. After entering their username and password, users are prompted to give permission to my app to create and modify a private playlist. 

After accepting, users are redirected to the page below, where they are able to name the new playlist, and are given options for customizing the type of songs that will be added to the playlist.

![image](https://user-images.githubusercontent.com/47374581/91737215-ca41bf80-eb7c-11ea-990c-5bcc5fa8007c.png)

After clicking continue, the playlist is generated and shown this page:

![image](https://user-images.githubusercontent.com/47374581/91737239-d0d03700-eb7c-11ea-92c7-013a5b4bc7e5.png)
