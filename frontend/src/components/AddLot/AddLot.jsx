import React, { useContext, useState } from "react";
import { observer } from "mobx-react-lite";
import { Context } from "../..";
import "./AddLot.css";

function AddLots() {
    const { storelots } = useContext(Context);
    const [file, setFile] = useState(null); // Используем null для файла
    const [startweight, setStartWeight] = useState(null);
    const [date, setDate] = useState("");
    const [code_KSSS_NB, setCode_KSSS_NB] = useState(null);
    const [code_KSSS_fuel, setCode_KSSS_fuel] = useState(null);
    const [current_weight, setCurrent_Weight] = useState(null);
    const [price, setPrice] = useState(null);
    const [priceforton, setPriceForTone] = useState(null);


    const handleSubmit = async (e) => {
        e.preventDefault();
        const lotData = {
            date: date,
            code_KSSS_NB: parseInt(code_KSSS_NB),
            code_KSSS_fuel: parseInt(code_KSSS_fuel),
            start_weight: parseInt(startweight),
            current_weight: parseInt(current_weight),
            status: "",
            price: parseInt(price),
            price_for_1ton: parseInt(priceforton)
        };
        await storelots.createLot(lotData);
        console.log(lotData);
    };


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

    const handleFileUpload = async () => {
        if (!file) {
            alert("Пожалуйста, выберите файл.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file); 

        try {
            await storelots.UploadFile(formData); 
            alert("Файл успешно загружен!");
            setFile(null); 
        } catch (error) {
            console.error("Ошибка при загрузке файла:", error);
            alert("Ошибка при загрузке файла.");
        }
    };

    return (
        <div className="Add">
            <div className="Add_Many_Lots">
                <h2>Добавление нескольких лотов</h2>
                <div className="AddFile" onClick={handleDivClick}>
                    <input
                        id="file-input"
                        type="file"
                        accept=".csv"
                        style={{ display: "none" }}
                        onChange={handleFileChange} // Исправлено: передаем handleFileChange
                    />
                    <p>{file ? `Выбран файл: ${file.name}` : "Нажмите для загрузки файла"}</p>
                </div>
                {file && (
                    <p onClick={handleFileUpload} style={{ marginTop: "10px", marginBottom: "10px"}}>
                        Загрузить файл
                    </p>
                )}
            </div>
            <div className="Add_One_Lot">
                <h2>Добавление одного лота</h2>
                <form className="AddLot" onSubmit={handleSubmit}>
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
                            value={code_KSSS_NB}
                            onChange={(e) => setCode_KSSS_NB(e.target.value)}
                        >
                            <option value="">Код КССС НБ</option>
                            <option value={1}>1</option>
                            <option value={2}>2</option>
                            <option value={3}>3</option>
                            <option value={4}>4</option>
                            <option value={5}>5</option>
                        </select>
                        <select
                            value={code_KSSS_fuel}
                            onChange={(e) => setCode_KSSS_fuel(e.target.value)}
                        >
                            <option value="">Код КССС Топлива</option>
                            <option value={1}>1</option>
                            <option value={2}>2</option>
                            <option value={3}>3</option>
                            <option value={4}>4</option>
                            <option value={5}>5</option>
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