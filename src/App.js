import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Base from "./components/Base";
import Home from "./components/Home";
import PlaylistFromArtist from "./components/PlaylistFromArtist";
import PlaylistFromGenre from "./components/PlaylistFromGenre";
import PlaylistFromTopTracks from "./components/PlaylistFromTopTracks";
import Success from "./components/Success";


function App() {
  return (
    <BrowserRouter>
      <Base />
      <Routes>
        <Route index element={<Home />} />
        <Route exact path="playlist-from-artist" element={<PlaylistFromArtist />} />
        <Route exact path="playlist-from-genre" element={<PlaylistFromGenre />} />
        <Route exact path="playlist-from-top-tracks" element={<PlaylistFromTopTracks />} />
        <Route exact path="success" element={<Success />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
