import React, { useState, useEffect } from "react";
import axiosInstance from "../services/AxiosInstance";
import { useNavigate } from "react-router-dom";
import SpotifyLogin from "./SpotifyLogin";
import capitalize from "../services/Capitalize";

const PlaylistFromGenre = () => {
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState("");
  const [error, setError] = useState("");
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitLoading, setSubmitLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await axiosInstance.get('check-authentication/');
        if (response.data.authenticated) {
          setAuthenticated(true);
          getGenres();
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

  const getGenres = async () => {
    try {
      const response = await axiosInstance.get("http://localhost:8000/api/genres/")
      setGenres(response.data.genres);
    } catch (error) {
      console.error("Error fetching genres:", error);
    }
  };

  const handleGenreChange = (e) => {
    setSelectedGenre(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitLoading(true);

    try {
      const response = await axiosInstance.post('create-genre-playlist/', {
        genre: selectedGenre
      });
      const playlistId = response.data.playlist.id;
      navigate("/success", { state: { playlistId } });
    } catch (error) {
      setError("Failed to create playlist.");
      console.error("An error occurred:", error);
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
        <h1>Playlist From Genre</h1>
        <p>
          This page will create a playlist for you consisting of music from the selected genre.
        </p>
      </div>
      <form className="mt-5" onSubmit={handleSubmit}>
        <div className="from-group">
          <label htmlFor="genreSelect" className="form-label">Select Genre</label>
          <select
            className="form-control"
            id="genreSelect"
            value={selectedGenre}
            onChange={handleGenreChange}
            required
          >
            <option value="" disabled>Select a genre</option>
            {genres.map((genre, index) => (
              <option key={index} value={genre}>{capitalize(genre)}</option>
            ))}
          </select>
        </div>
        {error && (
          <p className="text-danger">{error}</p>
        )}
        <button type="submit" className="btn btn-primary mt-3" disabled={submitLoading}>
          {submitLoading ? (
            <>
              Creating Playlist... <span className="spinner-border spinner-border-sm"></span>
            </>
          ) : (
            "Create Playlist"
          )}
        </button>
      </form>
    </div>
  );
};

export default PlaylistFromGenre;