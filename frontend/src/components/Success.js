import React from "react";
import { useLocation, Navigate } from "react-router-dom";

const Success = () => {
  const location = useLocation();
  const { state } = location;
  const playlistId = state?.playlistId

  if (!playlistId) {
    return <Navigate to="/" />;
  }

  return (
    <div className="container mt-5">
      <h1>Playlist Created Successfully!</h1>
      <p>Your playlist has been created. Check your Spotify account for the full playlist!</p>
      <iframe
        title="Spotify Playlist"
        src={`https://open.spotify.com/embed/playlist/${playlistId}?utm_source=generator`}
        width="100%"
        height="700px"
        frameBorder="0"
        allowFullScreen=""
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
        loading="lazy"
      ></iframe>
    </div>
  );
};

export default Success;