import React, { useState, useEffect } from "react";
import axiosInstance from "../services/AxiosInstance";
import { useNavigate } from "react-router-dom";
import SpotifyLogin from "./SpotifyLogin";

const PlaylistFromTopTracks = () => {
  const [timeframe, setTimeframe] = useState("");
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

  const handleTimeframeChange = (e) => {
    setTimeframe(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitLoading(true);

    try {
      const response = await axiosInstance.post('create-top-tracks-playlist/', {
        timeframe: timeframe
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
        <h1>Playlist From Top Tracks</h1>
        <p>
          This page will create a playlist of your top songs in the selected timeframe.
        </p>
      </div>
      <form className="mt-5" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="timeframeSelect" className="form-label">Select Timeframe</label>
          <select className="form-control" id="timeframeSelect" onChange={handleTimeframeChange}>
            <option value="short_term">Last 4 weeks</option>
            <option value="medium_term">Last 6 months</option>
            <option value="long_term">All time</option>
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

export default PlaylistFromTopTracks;