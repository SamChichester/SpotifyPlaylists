from django.urls import path
from .views import spotify_login, spotify_callback, create_artist_playlist, create_genre_playlist, create_top_tracks_playlist, check_authentication, get_genres

urlpatterns = [
    path('check-authentication/', check_authentication, name='check-authentication'),
    path('spotify-login/', spotify_login, name='spotify-login'),
    path('spotify-callback/', spotify_callback, name='spotify-callback'),
    path('genres/', get_genres, name='genres'),
    path('create-artist-playlist/', create_artist_playlist, name='create-artist-playlist'),
    path('create-genre-playlist/', create_genre_playlist, name='create-genre-playlist'),
    path('create-top-tracks-playlist/', create_top_tracks_playlist, name='create-top-tracks-playlist'),
]