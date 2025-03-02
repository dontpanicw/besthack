import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./BuyPage.css"
import { Context, storelots } from "../..";

function BuyPage() {
    const {number} = useParams();
    const {storelots} = useContext(Context);
    const [volume, setVolume] = useState(null);
    const [code_KSSS_NB, setCode_KSSS_NB] = useState(null);
    const [code_KSSS_fuel, setCode_KSSS_fuel] = useState(null);
    const [deliverytype, setDeliveryType] = useState('');

    useEffect(() => {
        storelots.showLot(number);
    }, [])

    const handleSubmit = () => {
        const orderData = {
                lot_number: number,
                volume: volume,
                delivery_type: deliverytype
        }
        storelots.makeOrder(orderData);
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
                <form>
                    <input
                    type="number"
                    placeholder="Объем"
                    value={volume}
                    onChange={(e) => setVolume(e.target.value)}
                    />
                    <input
                    type="number"
                    placeholder="Код КССС НБ"
                    value={code_KSSS_NB}
                    onChange={(e) => setCode_KSSS_NB(e.target.value)}
                    />
                    <input
                    type="number"
                    placeholder="Код КССС Топлива"
                    value={code_KSSS_fuel}
                    onChange={(e) => setCode_KSSS_fuel(e.target.value)}
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