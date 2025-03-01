import React from "react";
import Navbar from "./components/Navbar/Navbar";
import Homepage from "./components/HomePage/HomePage";
import Login from "./components/LoginPage/Login";
import Registration from "./components/LoginPage/Register/Register";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AddLot from "./components/AddLot/AddLot";

function App() {
  return (
    <>
    <Navbar/>

    <Routes>
      <Route path="/SearchPage" element={<Navbar/>}/>
      <Route path="/" element={<Homepage/>}/>
      <Route path="/Login" element={<Login/>}/>
      <Route path="/Registration" element={<Registration/>}/>
      <Route path="/AddLot" element={<AddLot/>}/>
    </Routes>

    </>
  );
}

export default App;
