import axios from "axios";
import React, { useState } from "react";
import { Link ,useHistory} from "react-router-dom";
import {auth} from "service/api/loginApi";
import "../assets/css/login.css"
function SignUp(){
    const [username,setUsername] = useState()
    const [password,setPassword] = useState()
    console.log(password,username);
    const history = useHistory()
    const handleSignUp =(e)=>{
    e.preventDefault()
    const data = {username:username,
      password:password}
      axios.post('/authenticator/register/',data).then(res=>{
        console.log(res)
        history.push('/login')
    })
   }
    return(
    <>
     <div className="container_signup">
     <form  className='form signup'>
        <div className='control'>
        <h3>Tạo tài khoản</h3>
        <div className="mb-3">
          <label>Tên đăng nhập</label>
          <input
            type="username"
            value={username}
            onChange={e=>setUsername(e.target.value)}
            className="form-control"
            
          />
        </div>
        <div className="mb-3">
          <label>Mật khẩu</label>
          <input
            type="password"
            className="form-control"
            onChange={e=>setPassword(e.target.value)}
          />
        </div>
        <div className="d-grid">
          <button type="submit" onClick={handleSignUp} className="btn btn-primary">
            Tạo tài khoản
          </button>
        </div>
        <p className="forgot-password text-right">
          Đã có tài khoản <Link to="/login">Đăng nhập?</Link>
        </p>
        </div>
      </form>
     </div>
    

    </>
    )
}
export default SignUp;