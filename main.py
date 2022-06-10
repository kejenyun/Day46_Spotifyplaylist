from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

## Scrapping
date = input(f"Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_webpage = response.text
#print(billboard_webpage)

soup =BeautifulSoup(billboard_webpage,"html.parser")
songs = soup.select(selector="li #title-of-a-story")
song_names = [song.getText().strip() for song in songs]

## Spotify Authentication
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI='https://example.com/callback'

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id= SPOTIPY_CLIENT_ID,
        client_secret= SPOTIPY_CLIENT_SECRET,
        redirect_uri= SPOTIPY_REDIRECT_URI,
        scope= 'playlist-modify-private',
        cache_path="token.txt",
        show_dialog=True,
        )
    )

user_id =sp.current_user()['id']


## Search songs by title
song_uris=[]
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track: {song} year: {year}", type='track')
    print(result)
    try:
        uri = result["tracks"]["items"][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped.")

## Create play list
billboard_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description='birthday play list')

#adding songs to play list
sp.playlist_add_items(playlist_id=billboard_playlist['id'], items=song_uris)


## spotify Document https://spotipy.readthedocs.io/en/2.13.0/#module-spotipy.client
