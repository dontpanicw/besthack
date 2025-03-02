import React, { useContext } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { store, Context } from "../..";
import { Navigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
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
            {store.isAuth == false ? (
                <div>
                <Link to='/Login'>
                    <button className="link_to_login">Войти</button>
                </Link>
                <Link to="/Register">
                    <button className="link_to_registr">Регистрация</button>
                </Link>
                </div>
            ): (
                <button 
                className="link_to_logout"
                onClick={() => {
                    store.logout();
                    return(
                        <Navigate to="/Login"/>
                    )
                }}
                >Выйти</button>
            )}
        </div>
    )
}

export default observer(Navbar);