import React, { useContext } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { store, Context } from "../..";
import "./Navbar.css";

function Navbar() {
    const { store } = useContext(Context);

    return (
        <div className="NavBar">
            <Link to='/'>
                <button className="link_to_main">Главная</button>
            </Link>
            {store.isAdmin ? (
                <Link to='/AddLot'>
                    <button className="link_to_lot">Добавить лот</button>
                </Link>
            ) : (<></>)}


            <Link to="/AccountPage">
                <img src={`${process.env.PUBLIC_URL}/User_alt_light.svg`} alt="" />
            </Link>
        </div>
    )
}

export default Navbar;