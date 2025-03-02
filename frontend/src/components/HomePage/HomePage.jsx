import React, { useEffect, useState } from "react";
import { useContext } from "react";
import "./Homepage.css";
import { Context, storelots } from "../..";
import { Link } from "react-router-dom";
import { flow } from "mobx";

function Homepage() {
    const { storelots } = useContext(Context);
    const [fueltype, setFuelType] = useState(null);
    const [nbname, setNbName] = useState(null);

    useEffect(() => {
        fetchLots();
    }, [])


    const fetchLots = async () => {
            await storelots.getLots();
    }
    const handleSubmit = async () => {
        await storelots.Filter({
            code_KSSS_NB: parseInt(nbname),
            code_KSSS_fuel: parseInt(fueltype)
        })
        console.log({
            code_KSSS_NB: parseInt(nbname),
            code_KSSS_fuel: parseInt(fueltype)
        })
    }

    return (
        <div className="homepage_container">
            <h1 className="Main">ЛУКОЙЛ</h1>
            <h2>FUEL EXCHANGE</h2>
            <div className="search-bar">
                <h2>Поиск по каталогу</h2>
                <div className="selectors">
                    <select value={fueltype} onChange={(e) => setFuelType(e.target.value)}>
                        <option key="">Вид топлива</option>
                        <option key="1" value={1}>1</option>
                        <option key="2" value={2}>2</option>
                        <option key="3" value={3}>3</option>
                        <option key="4" value={4}>4</option>
                        <option key="5" value={5}>5</option>
                    </select>
                    <select value={nbname} onChange={(e) => setNbName(e.target.value)}>
                        <option key="">Название нефтебазы</option>
                        <option key="1" value={1}>1</option>
                        <option key="2" value={2}>2</option>
                        <option key="3" value={3}>3</option>
                        <option key="4" value={4}>4</option>
                        <option key="5" value={5}>5</option>

                    </select>
                    <button onClick= {() => handleSubmit()} type="submit">Найти</button>
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
                            <li>{e.fuel_type}</li>
                            <li>{e.nb_name}</li>
                            <li>{e.region_nb}</li>
                        </ul>
                        <Link to={`/BuyPage/${e.number}`}>
                            <button className="product-button">Купить</button>
                        </Link>

                    </div>
                )) : (<></>)}



            </div>
        </div>
    )
}

export default Homepage;