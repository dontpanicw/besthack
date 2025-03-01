import React from "react";
import { observer } from "mobx-react-lite";
import "./AddLot.css";

function AddLots() {
    return (
        <div>
            <div className="Add_Many_Lots">
                <div className="AddFile">
                    <input 
                    type="file" 

                    />
                </div>
            </div>
            <div className="Add_One_Lot">
                <div className="AddLot">
                    {/* Первая строка - 2 инпута */}
                    <div className="input-row">
                        <input type="date" placeholder="Дата" />
                        <input type="date" placeholder="Дата" />
                    </div>
                    
                    {/* Вторая строка - 2 инпута */}
                    <div className="input-row">
                        <input type="number" placeholder="Код КССС НБ" />
                        <input type="number" placeholder="Код КССС Топлива" />
                    </div>
                    
                    {/* Третья строка - инпут, кнопка, инпут */}
                    <div className="input-row triple">
                        <input type="number" placeholder="Цена" />
                        <button>Добавить</button>
                        <input type="number" placeholder="Цена на 1 тонну" />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default observer(AddLots);