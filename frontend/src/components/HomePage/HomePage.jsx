import React from "react";
import "./Homepage.css";

function Homepage() {
    return (
        <div className="container">
        <h1>Заголовок</h1>
        <div className="search-bar">
            <select>
                <option key={""}>Вид топлива</option>
            </select>
            <select>
                <option key={""}>Регион нефтебазы</option>
            </select>
            <select>
                <option key={""}>Название нефтебазы</option>
            </select>
            <button type="submit">Найти</button>
        </div>
        <div className="product-grid">
            <div className="product">
                <h2>Новак</h2>
                <p>Новак - целева завдання. Незважаєте на нею.</p>
                <button className="product-button">Купить</button>
            </div>
            <div className="product">
                <h2>Новак</h2>
                <p>Новак - целева завдання. Незважаєте на нею.</p>
                <button className="product-button">Купить</button>
            </div>
            <div className="product">
                <h2>Новак</h2>
                <p>Новак - целева завдання. Незважаєте на нею.</p>
                <button className="product-button">Купить</button>
            </div>
            </div>
        </div>
    )
}

export default Homepage;