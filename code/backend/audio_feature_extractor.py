
def find_song(name, year = None, top_k = 5):
    import random
    from spotipy.oauth2 import SpotifyClientCredentials
    import spotipy as sp
    client_id = "0054a24f2fc643c69d56d020dd5f70be"
    client_secret = "98b4a4b772ad4eca934a92ca60c246a0"
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = sp.Spotify(client_credentials_manager=client_credentials_manager)
    song_data = {}

    if (year != None):
        results = sp.search(q= 'track: {}, year:{}'.format(name, year), limit=top_k)
    else:
        results = sp.search(q= 'track: {}'.format(name), limit=top_k)

    if results['tracks']['items'] == []:
        print("cant't find the track from Spotify database!")
        return None

    index = random.randrange(0, len(results))
    results = results['tracks']['items'][index]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = results['name']
    song_data['year'] = results['album']['release_date'][0:4]
    song_data['release_date'] = results['album']['release_date']

    song_data["artist_name"] = results['artists'][0]['name']  #choose the first artist if more than 1
    song_data["artist_id"] = results['artists'][0]['id']
    song_data["artist_url"] = results['artists'][0]['external_urls']['spotify']

    song_data['album_name'] = results['album']['name']
    song_data['album_id'] = results['album']['id']
    song_data["album_url"] = results['album']['external_urls']['spotify']

    search_features = ['danceability','energy', 'liveness', 'id']
    for key, value in audio_features.items():
        if key in search_features:
            if type(value) == float:
                value = value * 100
            song_data[key] = value

    song_data['duration_ms'] = results['duration_ms']
    song_data['popularity'] = results['popularity']
    song_data['track_trial'] = 'https://open.spotify.com/track/' + song_data['id']

    return song_data