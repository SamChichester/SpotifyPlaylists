import React from "react";

const SpotifyLogin = () => {
  const handleLogin = () => {
    const redirectUrl = encodeURIComponent(window.location.href);
    window.location.href = `http://localhost:8000/api/spotify-login/?redirect=${redirectUrl}`;
  };

  return (
    <button className="btn btn-primary" onClick={handleLogin}>
      Login with Spotify
    </button>
  )
};

export default SpotifyLogin;