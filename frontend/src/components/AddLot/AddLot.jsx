import React from "react";
import { useContext, useState } from "react";
import { observer } from "mobx-react-lite";
import { storelots, Context } from "../..";
import "./AddLot.css";

function AddLots() {
    const { storelots } = useContext(Context);
    const [file, setFile] = useState("");
    const [startweight, setStartWeight] = useState(null);
    const [date, setDate] = useState("");
    const [code_KSSS_NB, setCode_KSSS_NB] = useState(null);
    const [code_KSSS_fuel, setCode_KSSS_fuel] = useState(null);
    const [current_weight, setCurrent_Weight] = useState(null);
    const [price, setPrice] = useState(null);
    const [priceforton, setPriceForTone] = useState(null);

    const handleSubmit = async (e) => {
        const lotData = {
            date: date,
            code_KSSS_NB: parseInt(code_KSSS_NB),
            code_KSSS_fuel: parseInt(code_KSSS_fuel),
            start_weight: parseInt(startweight),
            current_weight: parseInt(current_weight),
            status: "",
            price: parseInt(price),
            price_for_1ton: parseInt(priceforton)
        }
        await storelots.createLot(lotData);
        console.log(lotData);
    }




    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            console.log("Выбран файл:", file.name);
            setFile(file);
        }
    };

    const handleDivClick = () => {
        document.getElementById("file-input").click();
    };

   /* const handleFileUpload = async (event) => {
        const file = event.target.files[0]; 
        const formData = new FormData();
        formData.append('file', file);
        await storelots.UploadFile(formData);
    } */

    return (
        <div className="Add">
            <div className="Add_Many_Lots">
                <h2>Добавление нескольких лотов</h2>
                <div className="AddFile" onClick={handleFileChange}>
                    <input
                        id="file-input"
                        type="file"
                        accept=".csv"
                        style={{ display: "none" }}
                        value={file}
                    />
                    <p onClick={async (e) => {
                        e.preventDefault();
                        await storelots.UploadFile(file);
                    }}>Нажмите для загрузки файла</p>
                </div>
            </div>
            <div className="Add_One_Lot">
                <h2>Добавление одного лота</h2>
                <form className="AddLot" onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit();}}>
                    <div className="input-row">
                        <input
                         type="date" 
                         placeholder="Дата"
                         value={date}
                         onChange={(e) => setDate(e.target.value)}
                          />
                        <input 
                        type="number" 
                        placeholder="Стартовый вес" 
                        value={startweight}
                        onChange={(e) => setStartWeight(e.target.value)}
                        />
                    </div>
                    <div className="input-row">
                        <select
                        type="number" 
                        value={code_KSSS_NB}
                        onChange={(e) => setCode_KSSS_NB(e.target.value)} 
                        >
                            <option key="">Код КССС НБ</option>
                            <option  key="1" value={1}>1</option>
                            <option key="1" value={2}>2</option>
                            <option key="1" value={3}>3</option>
                            <option key="1" value={4}>4</option>
                            <option key="1" value={5}>5</option>
                        </select>
                        <select 
                        type="number" 
                        value={code_KSSS_fuel}
                        onChange={(e) => setCode_KSSS_fuel(e.target.value)}
                         >
                            <option key="">Код КССС Топлива</option>
                            <option  key="1" value={1}>1</option>
                            <option key="1" value={2}>2</option>
                            <option key="1" value={3}>3</option>
                            <option key="1" value={4}>4</option>
                            <option key="1" value={5}>5</option>
                         </select>
                    </div>
                    <div className="input-row triple">
                        <input 
                        type="number" 
                        placeholder="Цена" 
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        />
                        <button type="submit">Добавить</button>
                        <input 
                        type="number" 
                        placeholder="Цена на 1 тонну" 
                        value={priceforton}
                        onChange={(e) => setPriceForTone(e.target.value)}
                        />
                    </div>
                </form>
            </div>
        </div>
    );
}

export default observer(AddLots);