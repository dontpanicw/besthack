import React, { useEffect } from "react";
import { useContext } from "react";
import "./Homepage.css";
import { Context, storelots } from "../..";
import { Link } from "react-router-dom";

function Homepage() {
    const {storelots} = useContext(Context);

    useEffect(() => {
        storelots.getLots();

    }, [])

    return (
        <div className="homepage_container">
            <h1 className="Main">Заголовок</h1>
            <div className="search-bar">
                <h2>Поиск по каталогу</h2>
                <div className="selectors">
                    <select>
                        <option key="">Вид топлива</option>
                    </select>
                    <select>
                        <option key="">Регион нефтебазы</option>
                    </select>
                    <select>
                        <option key="">Название нефтебазы</option>
                    </select>
                    <button type="submit">Найти</button>
                </div>
            </div>
        <h1>Каталог</h1>
        <div className="product-grid">
            {storelots.lots != null ? storelots.lots.map((e) => (
                <div className="product">
                <p>номер лота: {e.number}</p>
                <h2>{e.price_for_1ton} Руб.</h2>
                <h3>Остаток топлива</h3>

                <ul>
                    <li>Вид топлива</li>
                    <li>Название нефтебазы</li>
                    <li>Регион нефтебазы</li>
                </ul>
                <Link to={`/BuyPage/${e.number}`}>
                <button className="product-button">Купить</button>
                </Link>

            </div>
            )):(<></>)}
            
        
            
            </div>
        </div>
    )
}

export default Homepage;