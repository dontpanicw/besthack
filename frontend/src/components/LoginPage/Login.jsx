import React, { useState, useContext } from "react";
import { observer } from "mobx-react-lite";
import { Context } from "../..";
import { Navigate } from "react-router-dom";
import "./Login.css";

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({}); 
    const { store } = useContext(Context);


    const validateForm = () => {
        const newErrors = {};


        if (!email) {
            newErrors.email = "Поле email обязательно для заполнения";
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            newErrors.email = "Некорректный формат email";
        }

        if (!password) {
            newErrors.password = "Поле пароль обязательно для заполнения";
        } else if (password.length < 4) {
            newErrors.password = "Пароль должен содержать минимум 6 символов";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0; 
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

 
        if (!validateForm()) {
            return;
        }

        console.log("Submitting login...");
        const logindata = {
            username: email,
            password: password
        };

        try {
            await store.login(logindata);
        } catch (error) {
            alert("Ошибка авторизации: " + error.response?.data?.message);
        }
    };

    if (store.isAuth) {
        return <Navigate to={`/`} replace />;
    }

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
                        className={errors.email ? "error" : ""} 
                    />
                    {errors.email && <span className="error-message">{errors.email}</span>}

                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Пароль"
                        className={errors.password ? "error" : ""} 
                    />
                    {errors.password && <span className="error-message">{errors.password}</span>}
                    <button type="submit">Войти</button>
                </div>
            </form>
        </div>
    );
}

export default observer(Login);