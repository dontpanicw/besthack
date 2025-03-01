import React from "react";
import { Link, useNavigate } from 'react-router-dom'; 

function Navbar() {
    return (
        <div>
            <Link to="/SearchPage">
            <img src={`${process.env.PUBLIC_URL}/Search_light.svg`} alt=""/>
            </Link>
            <Link to="/AccountPage">
            <img src={`${process.env.PUBLIC_URL}/User_alt_light.svg`} alt=""/>
            </Link>
        </div>
    )
}

export default Navbar;