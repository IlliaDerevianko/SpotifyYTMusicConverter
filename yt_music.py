import time
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth 2.0 credentials file (downloaded from the Google Developers Console)
CLIENT_SECRETS_FILE = '/Users/illiaderevianko/Desktop/Python/SpotifyYTMusicConverter/client_secret_1.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials


def create_playlist(youtube, title, description='', cover_image_url=''):
    # Create the playlist
    request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description,
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
    )
    response = request.execute()
    # Return the playlist ID
    return response['id']


def search_and_add_songs_to_playlist(youtube, song_titles, playlist_id):
    n = len(song_titles)
    i = 0
    for song_title in song_titles:
        i += 1
        # Search for the song
        search_request = youtube.search().list(
            part='snippet',
            q=song_title,
            type='video',
            maxResults=1
        )
        search_response = search_request.execute()

        # Extract the video ID of the first search result
        video_id = search_response['items'][0]['id']['videoId']

        # Add the video to the playlist
        add_request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'position': 0,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        add_request.execute()
        print(f'Added {i}/{n} songs to the playlist.')
        time.sleep(2)

    print(f'Successfully added {len(song_titles)} songs to the playlist.')
    print(f'To view the playlist, go here: https://music.youtube.com/playlist?list={playlist_id}')
