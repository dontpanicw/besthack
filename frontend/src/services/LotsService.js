import Api from "../https/basichttps";
import api from "../https/https";

export default class LotsService{
    static async getLots(){
        return Api.get('/lots');
    }

    static async createLots(lotData){
        return api.post('/lot', lotData);
    }

    static async showLot(number){
        return api.get(`/lot/${number}`);
    }

    static async makeOrder(orderData){
        return api.post('/order', orderData);
    }

    static async Filter(filterData){
        return api.get('/filtered-lots', filterData, {
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Указываем нужный Content-Type
        }});
    }

    static async UploadFile(file){
        return api.post('/upload-csv', file, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    }
}