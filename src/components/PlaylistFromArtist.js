import React, { useState } from "react";

const PlaylistFromArtist = () => {
  const [artist, setArtist] = useState("");
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    setArtist(e.target.value)
  };

  const handleSubmit = (e) => {
    try {
      e.preventDefault();
      console.log("Artist name submitted:", artist);
    } catch (error) {
      setError(error.message)
      console.error("An error occurred:", error)
    }  
  };

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
        <button type="submit" className="btn btn-primary mt-3">
          Create Playlist
        </button>
      </form>
    </div>
  );
};

export default PlaylistFromArtist;