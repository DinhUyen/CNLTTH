/*!

=========================================================
* Light Bootstrap Dashboard React - v2.0.1
=========================================================

* Product Page: https://www.creative-tim.com/product/light-bootstrap-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { Component,useState, useEffect,useContext} from "react";
import { useLocation } from "react-router-dom";
import { Navbar, Container, Nav, Dropdown, Button } from "react-bootstrap";
import  './Navbar.css'
import axiosClient from "service/axiosClient";
import { GlobalState } from "layouts/Slidenav";

import routes from "routes.js";

function Header() {
  const {id,setId} = useContext(GlobalState)
  const location = useLocation();
  const [isShowMenu,setIsShowMenu] = useState(false)
 
  // const [dv,setDv] = useState([{
  //   name:"Tiểu đoàn 1",
  //   dv:[{
  //     nameDV:"c155",
  //     class:[
  //     "BĐATTT"
  //     ]
  // }]
  // }])
    const [dv,setDv] = useState([])
    const [listDv, setListDv] = useState([])
    useEffect(() => {
      async function getItem() {
        const res = await axiosClient.get("/Address/get-list-don-vi");
        setDv(res.data)  
      }
      getItem();
    }, []);
    const[tenDv, setTenDv] = useState()
    async function getTenDv(maDv){
      const res = await axiosClient.get(`/Address/get-name-don-vi/?donViID=${maDv}`)
      setTenDv(res.data.name)
    }
    function getId(id, name){
      // console.log(id)
      showMenu()
      setId(id)
      setTenDv(name)
     }
   console.log(dv) 

  
  const mobileSidebarToggle = (e) => {
    e.preventDefault();
    document.documentElement.classList.toggle("nav-open");
    var node = document.createElement("div");
    node.id = "bodyClick";
    node.onclick = function () {
      this.parentElement.removeChild(this);
      document.documentElement.classList.toggle("nav-open");
    };
    document.body.appendChild(node);
  };

  const getBrandText = () => {
    for (let i = 0; i < routes.length; i++) {
      if (location.pathname.indexOf(routes[i].layout + routes[i].path) !== -1) {
        return routes[i].name;
      }
    }
    return "Brand";
  };
  const showMenu = ()=>{
    setIsShowMenu(!isShowMenu)
  }
  return (
    <Navbar bg="light" expand="lg">
      <Container fluid>
        <div className="d-flex justify-content-center align-items-center ml-2 ml-lg-0">
          <Button
            variant="dark"
            className="d-lg-none btn-fill d-flex justify-content-center align-items-center rounded-circle p-2"
            onClick={mobileSidebarToggle}
          >
            <i className="fas fa-ellipsis-v"></i>
          </Button>
          <Navbar.Brand
            href="#home"
            onClick={(e) => e.preventDefault()}
            className="mr-2"
          >
            {getBrandText()}
          </Navbar.Brand>
        </div>
        <Navbar.Toggle aria-controls="basic-navbar-nav" className="mr-2">
          <span className="navbar-toggler-bar burger-lines"></span>
          <span className="navbar-toggler-bar burger-lines"></span>
          <span className="navbar-toggler-bar burger-lines"></span>
        </Navbar.Toggle>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="nav mr-auto" navbar>
            <div className="icon-down"  onClick={showMenu}>
              <input disabled
            type="username"  
            value={tenDv}
            // onChange={e=>setUsername(e.target.value)}
            className=" form-control email"
           />
            <div onClick={showMenu}><i className="nc-icon nc-stre-down "></i></div>
           
            </div>
          
            {isShowMenu &&  
            <div className="dropdown">
              <ul className="list">
                {dv?.data?.map((item,index)=>{
                  return (
                    <li className="item">
                    <p onClick={(e)=>getId(item.code, item.name)}>{item.name}</p>
                    <ul className="list-1">
                      {item?.data?.map((dd)=>{
                        return (
                        <li className="item-1">
                        <p  onClick={(e)=>getId(dd.code, dd.name)}>{dd.name}</p>
                        <ul className="list-2">
                          {dd?.data?.map((lop)=>{
                          return (
                            <li className="item-2">
                              <p  onClick={(e)=>getId(lop.code, lop.name)}>{lop.name}</p>
                            </li>
                          )
                          }
                       ) }
                        </ul>
                    </li>
                        )
                      }
                      )}
                    </ul>
                  </li>
                  )
                })}
                
              </ul>
            </div>}
          </Nav>
          <Nav className="ml-auto" navbar>
            <Nav.Item>
              <Nav.Link
                className="m-0"
                href="#pablo"
                onClick={(e) => e.preventDefault()}
              >
              </Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link
                className="m-0"
                href="/login"
              >
                
                <span className="no-icon"  >Log out</span>
                
             
              </Nav.Link>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
