import axios from "axios";
import { API_URL } from "./https";

const Api = axios.create({
    withCredentials: true,
    baseURL: API_URL
})

export default Api;