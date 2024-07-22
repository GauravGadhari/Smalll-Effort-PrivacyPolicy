from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import json

app = Flask(__name__)
ytmusic = YTMusic()

# Load authentication headers from JSON file
with open('headers_auth.json', 'r') as f:
    headers = json.load(f)

# Generic function to handle API responses
def handle_response(api_function, *args, **kwargs):
    try:
        response = api_function(*args, **kwargs)
        if response:
            return jsonify(response), 200
        else:
            return jsonify({'message': 'No data found.'}), 404
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

# API endpoint for search
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    return handle_response(
        ytmusic.search,
        data.get('query', ''),
        data.get('filter', ''),
        scope=data.get('scope', None),
        limit=data.get('limit', 10),
        ignore_spelling=data.get('ignoreSpelling', True)
    )

# API endpoint for search suggestions
@app.route('/suggestions', methods=['POST'])
def suggestions():
    data = request.json
    return handle_response(
        ytmusic.get_search_suggestions,
        data.get('query', ''),
        data.get('detailed_runs', False)
    )

# API endpoint for home page content
@app.route('/home', methods=['POST'])
def home():
    data = request.json
    return handle_response(ytmusic.get_home, limit=data.get('limit', 3))

# API endpoint for artist information
@app.route('/artist', methods=['POST'])
def artist():
    data = request.json
    return handle_response(ytmusic.get_artist, data.get('channelId', ''))

# API endpoint for artist albums
@app.route('/artist_albums', methods=['POST'])
def artist_albums():
    data = request.json
    return handle_response(
        ytmusic.get_artist_albums,
        data.get('channelId', ''),
        data.get('params', ''),
        limit=data.get('limit', 100),
        order=data.get('order', None)
    )

# API endpoint for album information
@app.route('/album', methods=['POST'])
def album():
    data = request.json
    return handle_response(ytmusic.get_album, data.get('browseId', ''))

# API endpoint for album browse ID
@app.route('/album_browse_id', methods=['POST'])
def album_browse_id():
    data = request.json
    return handle_response(ytmusic.get_album_browse_id, data.get('audioPlaylistId', ''))

# API endpoint for user information
@app.route('/user', methods=['POST'])
def user():
    data = request.json
    return handle_response(ytmusic.get_user, data.get('channelId', ''))

# API endpoint for song related content
@app.route('/song_related', methods=['POST'])
def song_related():
    data = request.json
    return handle_response(ytmusic.get_song_related, data.get('browseId', ''))

# API endpoint for lyrics
@app.route('/lyrics', methods=['POST'])
def lyrics():
    data = request.json
    return handle_response(ytmusic.get_lyrics, data.get('browseId', ''))

# API endpoint for taste profile
@app.route('/tasteprofile', methods=['GET'])
def tasteprofile():
    return handle_response(ytmusic.get_tasteprofile)

# API endpoint for mood categories
@app.route('/mood-categories', methods=['GET'])
def mood_categories():
    return handle_response(ytmusic.get_mood_categories)

# API endpoint for mood playlists
@app.route('/mood-playlists', methods=['POST'])
def mood_playlists():
    data = request.json
    return handle_response(ytmusic.get_mood_playlists, data.get('params', ''))

if __name__ == '__main__':
    app.run(debug=True)
