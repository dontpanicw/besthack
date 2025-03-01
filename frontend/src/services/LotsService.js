import Api from "../https/basichttps";

export default class LotsService{
    static async getLots(){
        return Api.get('/lots');
    }
}