# Spotify Playlist Creator Project

## Table of Contents
- [Description](#description)
- [Technologies Used](#technologies-used)
- [Demo & Features](#demo--features)
- [Reflection](#reflection)
- [Contact](#contact)
- [License](#license)


## Description
A while ago I was struggling with finding new music to listen to, so I created a python script that uses the Spotify Web API to create custom playlists based on my music taste.

Recently I decided to give the project a facelift by creating a React frontend for it.

## Technologies Used
- **Frontend:** Javascript, React, HTML, CSS, Bootstrap, React Bootstrap
- **Backend:** Python, Django, Django Rest Framework, Spotify Web API
- **Other:** Docker, Selenium (for testing)

## Demo & Features
### Video Demo
[![Project Demo](https://img.youtube.com/vi/LAdNBIWiJrk/0.jpg)](https://www.youtube.com/watch?v=LAdNBIWiJrk)
### Features
- [Spotify Login](#spotify-login)
- [Playlist From Artist](#playlist-from-artist)
- [Playlist From Genre](#playlist-from-genre)
- [Playlist From Top Tracks](#playlist-from-top-tracks)

#### Spotify Login
Users are directed to the Spotify login when they attempt to create a custom playlist. They will remain logged in until the Spotify access token expires.

![Project Screenshot](https://res.cloudinary.com/dvsvlcbec/image/upload/v1722842947/Screenshot_4_poxulo.png)

#### Playlist From Artist
Creates a playlist on the user's Spotify account consisting of songs similar to the specified artist.

![Project Screenshot](https://res.cloudinary.com/dvsvlcbec/image/upload/v1722843228/DEMOgymwebsite_2_evgsac.gif)

#### Playlist From Genre
Creates a playlist on the user's Spotify account consisting of the top songs of the chosen genre.

![Project Screenshot](https://res.cloudinary.com/dvsvlcbec/image/upload/v1722843332/DEMOgymwebsite_4_l9xzpo.gif)

#### Playlist From Top Tracks
Creates a playlist on the user's Spotify account consisting of their most listened songs during the selected time range.

![Project Screenshot](https://res.cloudinary.com/dvsvlcbec/image/upload/v1722843384/DEMOgymwebsite_6_est6xn.gif)


## Reflection
### What did I learn?
- Docker
- Selenium
- React Bootstrap

### What were some challenges?
I would say the biggest challenge was figuring out how to handle authentication with the Spotify Web API.

### How would I take this project further?
I would like to implement new ways to create playlists using the Spotify Web API; there are some really cool things to work with, like a song's [audio features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).

I would also really like to deploy this application when I have more time because I think it would be very helpful for those looking to find new music.

## Contact
LinkedIn - [Sam Chichester](https://www.linkedin.com/in/sam-chichester-48367123b/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.