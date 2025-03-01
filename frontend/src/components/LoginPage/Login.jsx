import React, { useState, useNavigate, useContext} from "react";
import { store, Context } from "../..";
import { observer } from "mobx-react-lite";

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { store } = useContext(Context);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Submitting login...");
        const logindata = {
            email: email,
            password: password
        }
        try {
            const response = await store.login(logindata);            
        } catch (error) {
            alert("Ошибка авторизации: " + error.response?.data?.message);
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
                <button type="submit">Войти</button>
                </div>
            </form>
        </div>
    )
}

export default observer(Login);