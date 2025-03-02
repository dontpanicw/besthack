import React, { useState, useNavigate, useContext} from "react";
import { store, Context } from "../../..";
import { observer } from "mobx-react-lite";
import { Navigate } from "react-router-dom";
import "./Register.css";

function Registration() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { store } = useContext(Context);
    const [isRegistered, setIsRegistered] = useState(false);
    const [errors, setErrors] = useState('');


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
            newErrors.password = "Пароль должен содержать минимум 4 символа";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0; 
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        const registerdata = {
            email: email,
            password: password
        }

        if(!validateForm()){
            return;
        }

        try {
            const response = await store.registration(registerdata); 
            setIsRegistered(true);

        } catch (error) {
            alert("Ошибка регистрации: " + error.response?.data);
        }
    };


   
    if (isRegistered) {
        return <Navigate to={`/Login`} replace />;
    }

    return (
        <div className="Login-form">
            <form onSubmit={handleSubmit}>
                <div className="container">
                <h3>Регистрация</h3>
                <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Адрес электронной почты"
                required
                />
                {errors.email && <span className="error-message">{errors.email}</span>}
                <input 
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                 placeholder="Пароль"
                required
                />
                {errors.password && <span className="error-message">{errors.password}</span>}
                <button type="submit">Зарегистрироваться</button>
                </div>
            </form>
        </div>
    )
}

export default observer(Registration);