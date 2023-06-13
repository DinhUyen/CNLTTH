import axios from "axios";

const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:8002',
    headers: {'content-type': 'application/json', 'Authorization':`${localStorage.getItem('token')}`}
  });
  export default axiosClient;