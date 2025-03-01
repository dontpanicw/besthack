import React, { useState, useNavigate, useContext} from "react";
import { store, Context } from "../../..";
import { observer } from "mobx-react-lite";
import "./Register.css";

function Registration() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { store } = useContext(Context);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const registerdata = {
            email: email,
            password: password
        }
        try {
            const response = await store.registration(registerdata);            
        } catch (error) {
            alert("Ошибка регистрации: " + error.response?.data);
        }
    };
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="container">
                <label htmlFor="email">Адрес электронной почты</label>
                <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                />
                <label htmlFor="password">Пароль</label>
                <input 
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                />
                <button type="submit">Зарегистрироваться</button>
                </div>
            </form>
        </div>
    )
}

export default observer(Registration);