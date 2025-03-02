import React from "react";
import Navbar from "./components/Navbar/Navbar";
import Homepage from "./components/HomePage/HomePage";
import Login from "./components/LoginPage/Login";
import Registration from "./components/LoginPage/Register/Register";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { store, Context } from ".";
import { useContext, useEffect } from "react";
import { setStore } from "./AuthManager";
import AddLot from "./components/AddLot/AddLot";
import BuyPage from "./components/BuyPage/BuyPage";
import RouteGuard from "./RouteGuard";
import Footer from "./components/Footer/Footer";

function App() {
  const { store } = useContext(Context);


  useEffect(() => {
    setStore(store);
  }, [store]);

  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/SearchPage" element={<Navbar />} />
        <Route path="/" element={<Homepage />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/Register" element={<Registration />} />
        <Route path="/AddLot" element={<AddLot />} />
        <Route path="/BuyPage/:number" element={<RouteGuard><BuyPage /></RouteGuard>} />
      </Routes>

   

    </>
  );
}

export default App;
