import React from "react";
import "./Footer.css"

function Footer() {
    return(
        <div className="footer">
            <h1>ЛУКОЙЛ</h1>
            <h3>Контакты</h3>
            <div className="email">
                <ul>
                    <li>LUKOIL@LUKOIL.RU</li>
                    <li>LIKOIL@LUKOIL.COM</li>
                </ul>
            </div>
            <div className="number">
                <ul>
                    <li>+74956274444</li>
                    <li>+74956289841</li>
                    <li>74956257016</li>
                </ul>
            </div>
        </div>
    )
}

export default Footer;