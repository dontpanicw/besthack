import React, { useEffect, useState } from "react";
import { useContext } from "react";
import "./Homepage.css";
import { Context, storelots } from "../..";
import { Link } from "react-router-dom";
import { flow } from "mobx";
import { observer } from "mobx-react-lite";


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
    const handleSubmit = () => {
        storelots.Filter({
            nb_name: nbname,
            fluel_type: fueltype,
        })
        console.log({
            nb_code: nbname,
            fuel_code: fueltype
        })
    }

    return (
        <div className="homepage_container">
            <h1 className="Main">ЛУКОЙЛ</h1>
            <h2 className="label">FUEL EXCHANGE</h2>
            <div className="search-bar">
                <h2>Поиск по каталогу</h2>
                <div className="selectors">
                    <select value={fueltype} onChange={(e) => setFuelType(e.target.value)}>
                        <option key="">Вид топлива</option>
                        <option key="1" value={"АИ-95"}>АИ-95</option>
                        <option key="2" value={"АИ-92"}>АИ-92</option>
                        <option key="3" value={"АИ-92 Экто"}>АИ-92 Экто</option>
                        <option key="4" value={"АИ-95 Экто"}>АИ-95 Экто</option>
                        <option key="5" value={"ДТ"}>ДТ</option>
                    </select>
                    <select value={nbname} onChange={(e) => setNbName(e.target.value)}>
                        <option key="">Название нефтебазы</option>
                        <option key="1" value={"Нефтебаза_1"}>Нефтебаза_1</option>
                        <option key="2" value={"Нефтебаза_2"}>Нефтебаза_2</option>
                        <option key="3" value={"Нефтебаза_3"}>Нефтебаза_3</option>
                        <option key="4" value={"Нефтебаза_4"}>Нефтебаза_4</option>
                        <option key="5" value={"Нефтебаза_5"}>Нефтебаза_5</option>

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
                        <div className="button-container">
                        <Link to={`/BuyPage/${e.number}`}>
                            <button className="product-button">Купить</button>
                        </Link>
                        </div>

                    </div>
                )) : (<></>)}



            </div>
        </div>
    )
}

export default observer(Homepage);