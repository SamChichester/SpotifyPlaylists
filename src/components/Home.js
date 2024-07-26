import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="container mt-5">
      <h1>Welcome to Spotify Playlists Creator!</h1>
      <p>The following pages will help you create Spotify playlists customized for you!</p>
      <div className="mt-5">
        <Link to="playlist-from-artist">Create a playlist similar to a specific artist</Link>
      </div>
    </div>
  );
};

export default Home;