import React, { useState, useNavigate, useContext} from "react";
import { store, Context } from "../..";
import { observer } from "mobx-react-lite";
import "./Login.css";

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { store } = useContext(Context);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Submitting login...");
        const logindata = {
            username: email,
            password: password
        }
        try {
            const response = await store.login(logindata);            
        } catch (error) {
            alert("Ошибка авторизации: " + error.response?.data?.message);
        }
    };
    return (
        <div className="Login-form">
            <form onSubmit={handleSubmit}>
                <div className="container">
                <h3>Вход</h3>
                <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Адрес электронной почты"
                required
                />
                <input 
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Пароль"
                required
                />
                <button type="submit">Войти</button>
                </div>
            </form>
        </div>
    )
}

export default observer(Login);