import React from "react";
import Navbar from "./components/Navbar/Navbar";
import Homepage from "./components/HomePage/HomePage";
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <>
    <Navbar/>

    <Routes>
      <Route path="/SearchPage" element={<Navbar/>}/>
      <Route path="/" element={<Homepage/>}/>
    </Routes>

    </>
  );
}

export default App;
