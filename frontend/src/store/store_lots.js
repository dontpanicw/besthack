import { makeAutoObservable } from "mobx";
import {makePersistable} from "mobx-persist-store";
import LotsService from "../services/LotsService";

export default class StoreLots {
    lots = [];

    constructor() {
        makeAutoObservable(this);
        makePersistable(this, {
            name: "StoreLots",
            properties: ["lots"], 
            storage: window.localStorage, 
        });
    }

    setLots(lots){
        this.lots = lots;
    }

    async getLots(){
        try{
            const response = await LotsService.getLots();
            console.log(response);
            this.setLots(response.data);
        } catch(e){
            console.log(e.response?.data?.message);
        }
    }
    

   

}