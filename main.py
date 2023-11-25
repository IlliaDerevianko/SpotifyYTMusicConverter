from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from spotify import get_spotify_playlists, get_tracks_from_playlist, get_playlist
from yt_music import create_playlist, search_and_add_songs_to_playlist, authenticate

# Authenticate and create a YouTube client
youtube = build('youtube', 'v3', credentials=authenticate())

spotify_playlists = get_spotify_playlists()
print('Choose a playlist:')
for i, playlist in enumerate(spotify_playlists):
    print(f'{i + 1}. {playlist["name"]}')
playlist_index = int(input('Enter the number of the playlist (or enter 0 if the desired playlist is not in the list): ')) - 1
if playlist_index == -1:
    print('Copy and paste the Spotify playlist link here: ')
    playlist_link = input()
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    playlist = get_playlist(playlist_id)
else:
    playlist = spotify_playlists[playlist_index]

print(f'You chose "{playlist["name"]}". We will now create a YouTube playlist with the same name and add the songs to'
      f' it. Would you like to change the name of the playlist?\nY/N: ')
change_name = input()
if change_name.lower() == 'y':
    yt_playlist_name = input('Enter the name of the YouTube playlist: ')
else:
    yt_playlist_name = playlist['name']
# replace all < with the unicode equivalent u+25c1 and > with u+25b7 to avoid errors
yt_playlist_name = yt_playlist_name.replace('<', '\u25c1').replace('>', '\u25b7')
tracks = get_tracks_from_playlist(playlist['id'])
track_names = [f'{track["name"]} {track["artists"][0]["name"]}' for track in tracks]

yt_playlist_id = create_playlist(youtube, yt_playlist_name)
if yt_playlist_id:
    print(f'Created YouTube playlist "{yt_playlist_name}" with ID: {yt_playlist_id}')
    search_and_add_songs_to_playlist(youtube, track_names, yt_playlist_id)
else:
    print('Failed to create YouTube playlist.')

