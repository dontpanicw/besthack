import api from "../https/https";

export default class AuthService{
    static async Register(registerData){
        return api.post('/register', registerData);
    }

    static async Login(loginData){
        return api.post('/token', loginData);
    }

    static async CheckAdmin(){
        return api.get('/users/me');
    }
}