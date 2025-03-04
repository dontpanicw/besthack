import api from "../https/https";

export default class AuthService{
    static async Register(registerData){
        return api.post('/auth/register', registerData);
    }

    static async Login(loginData){
        return api.post('/auth/token', loginData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Указываем нужный Content-Type
        }
    })
    }

    static async CheckAdmin(){
        return api.get('/auth/me/admin-status');
    }
}