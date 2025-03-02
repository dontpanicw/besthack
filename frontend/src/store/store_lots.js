import { makeAutoObservable } from "mobx";
import {makePersistable} from "mobx-persist-store";
import LotsService from "../services/LotsService";

export default class StoreLots {
    lots = [];
    lot = {};
    filterlots =[];

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

    Filter(filterData) {
        try {
            this.filterlots = this.lots.filter(lot => {
                const matchesCodeKSSSNB = filterData.nb_name ? lot.nb_name === filterData.nb_name : true;
                const matchesCodeKSSSFluel = filterData.fluel_type ? lot.fluel_type === filterData.fluel_type : true;
                return matchesCodeKSSSNB && matchesCodeKSSSFluel;
            });
            this.setLots(this.filterlots);
            console.log("Filtered lots:", this.filterlots);
        } catch (e) {
            console.log("Error during filtering:", e);
        }
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
            this.setLot(response.data);
            console.log(response)
        } catch (e) {
            console.log(e.response?.data?.message)
        }
    }

    async makeOrder(orderData){
        try{
            const response = await LotsService.makeOrder(orderData);
            console.log(response);
        } catch (e) {
            console.log(e.response.details?.msg)
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