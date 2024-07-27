import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Base from "./components/Base";
import Home from "./components/Home";
import PlaylistFromArtist from "./components/PlaylistFromArtist";
import Success from "./components/Success";


function App() {
  return (
    <BrowserRouter>
      <Base />
      <Routes>
        <Route index element={<Home />} />
        <Route exact path="playlist-from-artist" element={<PlaylistFromArtist />} />
        <Route exact path="success" element={<Success />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
