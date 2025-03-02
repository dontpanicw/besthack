import Api from "../https/basichttps";
import api from "../https/https";

export default class LotsService{
    static async getLots(){
        return Api.get('/lots');
    }

    static async createLots(lotData){
        return api.post('/lots', lotData);
    }

    static async showLot(number){
        return api.get(`/lots/${number}`);
    }

    static async makeOrder(orderData){
        return api.post('/orders/order', orderData);
    }

    static async Filter(filterData){
        return api.get('/lots/filtered-lots', filterData);
    }

    static async UploadFile(file){
        return api.post('/lots/upload/upload-csv', file, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    }
}