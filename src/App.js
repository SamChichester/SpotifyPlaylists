import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Base from "./components/Base";
import Home from "./components/Home";


function App() {
  return (
    <BrowserRouter>
      <Base />
      <Routes>
        <Route index element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
