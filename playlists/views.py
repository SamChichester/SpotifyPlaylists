import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
import json
import random


timeframes = {
    'short_term': 'in the last 4 weeks',
    'medium_term': 'in the last 6 months',
    'long_term': 'of all time'
}


def spotify_login(request):
    redirect_url = request.GET.get('redirect', '/')
    auth_url = (
        'https://accounts.spotify.com/authorize?'
        'response_type=code'
        '&client_id={}'
        '&redirect_uri={}'
        '&scope=playlist-modify-public user-top-read'
        '&state={}'.format(
            settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_REDIRECT_URI, redirect_url
        )
    )
    return redirect(auth_url)


def spotify_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    token_url = 'https://accounts.spotify.com/api/token'

    response = requests.post(
        token_url,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
    )
    response_data = response.json()
    access_token = response_data.get('access_token')
    refresh_token = response_data.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

    profile_url = 'https://api.spotify.com/v1/me'
    profile_response = requests.get(
        profile_url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    profile_data = profile_response.json()

    user_id = profile_data.get('id')

    request.session['spotify_user_id'] = user_id
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token

    if state:
        return redirect(state)
    return JsonResponse(response_data)


def refresh_access_token(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        return None

    refresh_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(
        refresh_url,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
    )

    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens.get('access_token')
        if new_access_token:
            request.session['access_token'] = new_access_token
            return new_access_token
    else:
        error_response = response.json()
        if response.status_code == 400 and error_response.get('error') == 'invalid_grant':

            request.session.pop('access_token', None)
            request.session.pop('refresh_token', None)

    return None


def make_request(request, url, headers, params=None):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 401:  # Token expired
        new_access_token = refresh_access_token(request)
        if new_access_token:
            headers['Authorization'] = f'Bearer {new_access_token}'
            response = requests.get(url, headers=headers, params=params)
    return response


def create_artist_playlist(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token found in session'}, status=401)

    user_id = request.session.get('spotify_user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID not found'}, status=401)

    try:
        data = json.loads(request.body)
        artist_name = data.get('artist_name')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'No artist name provided'}, status=400)

    search_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    search_response = make_request(request, search_url, headers, params={'q': artist_name, 'type': 'artist'})
    search_data = search_response.json()

    if not search_data['artists']['items']:
        return JsonResponse({'error': 'Artist not found'}, status=404)

    artist = search_data['artists']['items'][0]
    artist_id = artist['id']
    artist_name = artist['name']

    related_artists_url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    related_artists_response = make_request(request, related_artists_url, headers)
    related_artists_data = related_artists_response.json()

    if not related_artists_data['artists']:
        return JsonResponse({'error': 'No related artists found'}, status=404)

    related_artist_ids = [artist['id'] for artist in related_artists_data['artists']]

    tracks = []
    for artist_id in related_artist_ids:
        top_tracks_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
        top_tracks_response = make_request(request, top_tracks_url, headers, params={'market': 'US'})
        top_tracks_data = top_tracks_response.json()

        if 'tracks' in top_tracks_data:
            tracks.extend(top_tracks_data['tracks'])

    if not tracks:
        return JsonResponse({'error': 'No tracks found for related artists'}, status=404)

    random_tracks = random.sample(tracks, min(100, len(tracks)))

    create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    create_playlist_response = requests.post(
        create_playlist_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={
            'name': f'Similar to {artist_name}',
            'description': f'Playlist consisting of artists similar to {artist_name}',
            'public': True
        }
    )
    playlist_data = create_playlist_response.json()

    if 'id' not in playlist_data:
        return JsonResponse({'error': 'Failed to create playlist'}, status=500)

    playlist_id = playlist_data['id']

    add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    tracks_uris = [track['uri'] for track in random_tracks]
    add_tracks_response = requests.post(
        add_tracks_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={'uris': tracks_uris}
    )

    return JsonResponse({'playlist': {'id': playlist_id}})


def create_genre_playlist(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token found in session'}, status=401)

    user_id = request.session.get('spotify_user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID not found'}, status=401)

    try:
        data = json.loads(request.body)
        genre = data.get('genre')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'No genre provided'}, status=400)

    recommendations_url = 'https://api.spotify.com/v1/recommendations'
    headers = {'Authorization': f'Bearer {access_token}'}
    recommendations_response = make_request(request, recommendations_url, headers,
                                            params={'seed_genres': genre, 'limit': 100})
    recommendations_data = recommendations_response.json()

    if 'tracks' not in recommendations_data or len(recommendations_data['tracks']) == 0:
        return JsonResponse({'error': 'No tracks found for the selected genre'}, status=404)

    track_uris = [track['uri'] for track in recommendations_data['tracks']]

    create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    create_playlist_response = requests.post(
        create_playlist_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={
            'name': f'Top Tracks of {genre.capitalize()}',
            'description': f'Playlist of top tracks in the {genre} genre',
            'public': True
        }
    )
    playlist_id = create_playlist_response.json()['id']

    add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    add_tracks_response = requests.post(
        add_tracks_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={'uris': track_uris}
    )

    return JsonResponse({'playlist': {'id': playlist_id}})


def get_genres(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token found in session'}, status=401)

    genres_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = make_request(request, genres_url, headers)

    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch genres'}, status=response.status_code)

    genres = response.json().get('genres', [])
    return JsonResponse({'genres': genres})


def create_top_tracks_playlist(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token found in session'}, status=401)

    user_id = request.session.get('spotify_user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID not found'}, status=401)

    try:
        data = json.loads(request.body)
        timeframe = data.get('timeframe')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if not timeframe:
        timeframe = 'short_term'
    headers = {'Authorization': f'Bearer {access_token}'}

    # First request: Get the first 50 top tracks
    top_tracks_url = f'https://api.spotify.com/v1/me/top/tracks?time_range={timeframe}&limit=50'
    top_tracks_response_1 = make_request(request, top_tracks_url, headers)
    top_tracks_data_1 = top_tracks_response_1.json()['items']

    # Second request: Get the next 50 top tracks
    top_tracks_url = f'https://api.spotify.com/v1/me/top/tracks?time_range={timeframe}&limit=50&offset=50'
    top_tracks_response_2 = make_request(request, top_tracks_url, headers)
    top_tracks_data_2 = top_tracks_response_2.json()['items']

    top_tracks_data = top_tracks_data_1 + top_tracks_data_2

    if len(top_tracks_data) == 0:
        return JsonResponse({'error': 'No top tracks found'}, status=404)

    track_uris = [track['uri'] for track in top_tracks_data]

    create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    create_playlist_response = requests.post(
        create_playlist_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={
            'name': f'My Top Tracks',
            'description': f'Playlist of top tracks {timeframes[timeframe]}',
            'public': True
        }
    )
    playlist_id = create_playlist_response.json()['id']

    add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    add_tracks_response = requests.post(
        add_tracks_url,
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        json={'uris': track_uris}
    )

    return JsonResponse({'playlist': {'id': playlist_id}})


def check_authentication(request):
    if request.session.get('access_token'):
        return JsonResponse({'authenticated': True})
    return JsonResponse({'authenticated': False}, status=401)


