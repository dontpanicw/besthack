import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./BuyPage.css"
import { Context, storelots } from "../..";

function BuyPage() {
    const {number} = useParams();
    const {storelots} = useContext(Context);
    const [volume, setVolume] = useState(null);
    const [deliverytype, setDeliveryType] = useState('');

    useEffect(() => {
        fetchLot();
    }, [])

    const fetchLot = async () => {
        await storelots.showLot(number);
    }

    const handleSubmit = async () => {
        const orderData = {
                lot_number: parseInt(number),
                volume: parseInt(volume),
                delivery_type: deliverytype
        }
        await storelots.makeOrder(orderData);
    }

 
    return (
        <div className="BuyPage">
            <div className="Info">
                <h3>Подробная информация о лоте</h3>
                <div className="info_about">
                    <ul>
                        <li>Номер:{storelots.lot?.number}</li>
                        <li>Дата:{storelots.lot?.date}</li>
                        <li>Код КССС НБ:{storelots.lot?.code_KSSS_NB}</li>
                        <li>Код КССС Топлива:{storelots.lot?.code_KSSS_fuel}</li>
                        <li>Стартовый вес:{storelots.lot?.start_weight}</li>
                        <li>Доступный остаток:{storelots.lot?.current_weight}</li>
                        <li>Статус:{storelots.lot?.status}</li>
                        <li>Цена лога:{storelots.lot?.price}</li>
                        <li>Цена за одну тонну:{storelots.lot?.price_for_1ton}</li>
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
                    <select
                    placeholder="Тип доставки"
                    value={deliverytype}
                    onChange={(e) => setDeliveryType(e.target.value)}
                    >
                        <option key="1" value="самовывоз">Самовывоз</option>
                        <option key="2" value="доставка">Доставка</option>
                    </select>
                    <button type="submit">Заказать</button>
                </form>
            </div>
        </div>
    )
}

export default BuyPage;