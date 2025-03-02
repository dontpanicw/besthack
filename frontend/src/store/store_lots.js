import { makeAutoObservable } from "mobx";
import {makePersistable} from "mobx-persist-store";
import LotsService from "../services/LotsService";

export default class StoreLots {
    lots = [];
    lot = {};

    constructor() {
        makeAutoObservable(this);
        makePersistable(this, {
            name: "StoreLots",
            properties: ["lots", "lot"], 
            storage: window.localStorage, 
        });
    }

    setLots(lots){
        this.lots = lots;
    }

    setLot(lot){
        this.lot = lot;
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

    async createLot(lotData){
        try{
            const response = await LotsService.createLots(lotData);
            console.log(response);
        } catch(e) {
            console.log(e.response?.data?.message)
        }
    }
    
    async showLot(number){
        try{
            const response = await LotsService.showLot(number);
            console.log(response);
            this.setLot(response.data);
        } catch (e) {
            console.log(e.response?.data?.message)
        }
    }

    async makeOrder(orderData){
        try{
            const response = await LotsService.makeOrder(orderData);
            console.log(response);
        } catch (e) {
            console.log(e.response?.data?.message)
        }
    }

    async Filter(filterData){
        try{
            const response = await LotsService.Filter(filterData);
            this.setLots(response.data);
            console.log(response);
        } catch(e) {
            console.log(e.response?.detail?.msg)
        }
    }

    async UploadFile(file){
        try{
            const response = await LotsService.UploadFile(file);
            console.log(response)
        } catch (e) {
            console.log(e.response)
        }
    }

}