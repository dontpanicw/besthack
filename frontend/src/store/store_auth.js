import { makeAutoObservable } from "mobx";
import AuthService from "../services/AuthService";
import {makePersistable} from "mobx-persist-store";

export default class Store {
    user = {
        email: ''
    };
    isAuth = false;
    isAdmin = false;

    constructor() {
        makeAutoObservable(this);
        makePersistable(this, {
            name: "Store",
            properties: ["user", 'isAuth', 'isAdmin'], // Properties to persist
            storage: window.localStorage, // Use localStorage for persistence
        });
    }

    setAuth(bool) {
        this.isAuth = bool;
    }

    setUser(user) {
        this.user = user;
    }

    setAdmin(bool) {
        this.isAdmin = bool;
    }


    async login(loginData) {
        try {
            const response = await AuthService.Login(loginData);
            console.log(response);
            localStorage.setItem('token', response.data.access_token);
            this.setAuth(true);
    
            // Получаем данные пользователя сразу после успешного входа
            await this.checkAdmin();
        } catch (e) {
            alert(e.response?.data?.detail);
        }
    }

    async registration(registerData) {
        try {
            const response = await AuthService.Register(registerData);
            console.log(response);
            this.setAuth(true);
        } catch (e) {
            console.log(e.response?.data?.detail);
        }
    }

    async checkAdmin(){
        try{
            const response = await AuthService.CheckAdmin();
            console.log(response);
            this.setAdmin(response.is_admin);
        } catch (e) {
            console.log(e.response?.data?.detail)
        }

    }

}