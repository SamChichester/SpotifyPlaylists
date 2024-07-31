import React, { useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const Base = () => {
  useEffect(() => {
    const fetchCsrfToken = async() => {
      try {
        const response = await axios.get('http://localhost:8000/csrf/', { withCredentials: true });
        const csrfToken = response.data.csrfToken;
        Cookies.set('csrftoken', csrfToken);
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    };

    fetchCsrfToken();
  }, []);

  return (
    <Navbar expand="lg" className="spotify-navbar">
      <Container>
        <Navbar.Brand href="/">Spotify Playlists</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="playlist-from-artist">Playlist From Artist</Nav.Link>
            <Nav.Link href="playlist-from-genre">Playlist From Genre</Nav.Link>
            <Nav.Link href="playlist-from-top-tracks">Playlist From Top Tracks</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Base;