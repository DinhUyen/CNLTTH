import axios from "axios";
import React, { useState } from "react";
import { Link ,useHistory} from "react-router-dom";
import "../assets/css/login.css"
function SignIn(){
  const [username,setUsername] = useState()
  const [password,setPassword] = useState()
  console.log(password,username);
  const history = useHistory()
   const handleLogin =(e)=>{
    e.preventDefault()
    const data = {username:username,
      password:password}
    axios.post('http://127.0.0.1:8002/authenticator/login/',data).then(res=>{
      console.log(res)
      localStorage.setItem("token","CNLTTH "+res.data.access)
      history.push({
        pathname:'/admin/dashboard',
        refresh:true
      })
    })
   }
    return(
    <>
    <div className="container_signin">
    <form  className='form signup'>
        <div className='control'>
        <h3>Đăng nhập</h3>
        <div className="mb-3">
          
          <label>Tên đăng nhập</label>
          <input
            type="username"
            
            className="form-control password"
            onChange={e=>setUsername(e.target.value)}
            value={username}
          />
        </div>
        <div className="mb-3">
          
          <label>Mật khẩu</label>
          <input
            type="password"
            
            className="form-control password"
            onChange={e=>setPassword(e.target.value)}
          />
        </div>

        <div className="d-grid">
          <button type="submit" onClick={handleLogin} className="btn btn-primary submit">
            Submit
          </button>
        </div>
        </div>
        {/* <p className="forgot-password text-right">
          Create <Link to="/signup">Account</Link>
        </p> */}

      </form>
    </div>
   

    </>
    )
}
export default SignIn;
