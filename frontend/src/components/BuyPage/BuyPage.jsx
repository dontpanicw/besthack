import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./BuyPage.css"
import { Context, storelots } from "../..";
import { observer } from "mobx-react-lite";

function BuyPage() {
    const {number} = useParams();
    const {storelots} = useContext(Context);
    const [volume, setVolume] = useState(null);
    const [deliverytype, setDeliveryType] = useState('');
    const [error, setError] = useState('');

    const fetchLot = async () => {
        try {
            await storelots.showLot(number);
        } catch (error) {
            console.error("Ошибка при загрузке лота:", error);
        }
    }

    useEffect(() => {
        fetchLot();
    }, [])


    useEffect(() => {
        if (storelots.lot.current_weight < volume) {
            setError("Значение больше допустимого");
        } else {
            setError(""); 
        }
    }, [volume, storelots.lot.current_weight]);

    const handleSubmit = async (e) => {
        const orderData = {
                lot_number: parseInt(number),
                volume: parseInt(volume),
                delivery_type: deliverytype
        }
        try{
            await storelots.makeOrder(orderData);
        } catch(e) {
            return alert(e);
        }
        
    }

 
    return (
        <div className="BuyPage">
            <div className="Info">
                <h3>Подробная информация о лоте</h3>
                <div className="info_about">
                    <ul>
                        <li>Номер:{storelots.lot.number}</li>
                        <li>Дата:{storelots.lot.date}</li>
                        <li>Код КССС НБ:{storelots.lot.code_KSSS_NB}</li>
                        <li>Код КССС Топлива:{storelots.lot.code_KSSS_fuel}</li>
                        <li>Стартовый вес:{storelots.lot.start_weight}</li>
                        <li>Доступный остаток:{storelots.lot.current_weight}</li>
                        <li>Статус:{storelots.lot.status}</li>
                        <li>Цена лога:{storelots.lot.price}</li>
                        <li>Цена за одну тонну:{storelots.lot.price_for_1ton}</li>
                    </ul>
                </div>
            </div>
            <div className="BuyForm">
                <h3>Оформление заказа</h3>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit();
                }}>
                    <input
                    type="number"
                    placeholder="Объем"
                    value={volume}
                    onChange={(e) => setVolume(e.target.value)}
                    />
                    {error? (
                        <label className="error-message">{error}</label>
                    ): (<></>)}
                    <select
                    placeholder="Тип доставки"
                    value={deliverytype}
                    onChange={(e) => setDeliveryType(e.target.value)}
                    >
                        <option key="1" value="самовывоз">Самовывоз</option>
                        <option key="2" value="доставка">Доставка</option>
                    </select>
                    <button type="submit" disabled={!!error}>Заказать</button>
                </form>
            </div>
        </div>
    )
}

export default observer(BuyPage);