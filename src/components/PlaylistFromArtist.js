import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from 'js-cookie';
import { useNavigate } from "react-router-dom";
import SpotifyLogin from "./SpotifyLogin";

const PlaylistFromArtist = () => {
  const [artist, setArtist] = useState("");
  const [error, setError] = useState("");
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitLoading, setSubmitLoading] = useState(false);
  const navigate = useNavigate();
  

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/check-authentication/', {
          withCredentials: true
        })
        if (response.data.authenticated) {
          setAuthenticated(true);
        } else {
          setAuthenticated(false);
        }
      } catch (error) {
        console.error("Error checking authentication:", error);
        setAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuthentication();
  }, []);

  const handleInputChange = (e) => {
    setArtist(e.target.value)
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitLoading(true);

    const csrfToken = Cookies.get('csrftoken');

    try {
      const response = await axios({
        method: 'post',
        url: 'http://localhost:8000/api/create-playlist/',
        data: { artist_name: artist },
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true
      });
      
      const playlistId = response.data.playlist.id
      navigate("/success", { state: { playlistId } });
    } catch (error) {
      setError("Failed to create playlist.")
      console.error("An error occurred:", error)
    } finally {
      setSubmitLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div className="d-flex flex-column align-items-center mt-5">
        <p>You need to log in to create a playlist.</p>
        <SpotifyLogin />
      </div>
    )
  }

  return (
    <div className="container mt-5">
      <div>
        <h1>Playlist From Artist</h1>
        <p>
          This page will create a playlist for you consisting of songs similar to the artist you specified. 
          The input box will find the artist closest to what is typed.
          This will not work for very small artists.
        </p>
      </div>
      <form className="mt-5" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="artistName" className="form-label">Artist Name</label>
          <input 
            type="text" 
            className="form-control" 
            id="artistName" 
            value={artist}
            onChange={handleInputChange}
            placeholder="Enter artist name."
            required
          />
        </div>
        {error && (
          <p className="text-danger">{error}</p>
        )}
        <div className="d-flex align-items-center mt-3">
          <button type="submit" className="btn btn-primary" disabled={submitLoading}>
            Create Playlist
          </button>
          {submitLoading && (
            <div className="spinner-border spinner-border-sm ms-2" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default PlaylistFromArtist;