import axiosClient from "service/axiosClient";
import axios from "axios";
const auth = {
    login:(path,data)=>{
        axios.post(path,data).then(res=>{
            console.log(res.data);
        })
    }
}

export { auth}