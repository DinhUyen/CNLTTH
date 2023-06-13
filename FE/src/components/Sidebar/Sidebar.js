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
import React, { Component, useEffect, useState,useContext } from "react";
import { useLocation, NavLink } from "react-router-dom";
import axiosClient from "service/axiosClient";
import { Nav } from "react-bootstrap";
import { GlobalState } from "layouts/Slidenav";
import logo from "assets/img/reactlogo.png";

function Sidebar({ color, image, routes }) {
  const {MaDV, setMADV} = useContext(GlobalState)
  const [role,setRole] = useState()
  const location = useLocation();
  const activeRoute = (routeName) => {
    return location.pathname.indexOf(routeName) > -1 ? "active" : "";
  };
// API get permission
useEffect(()=>{
  async function getPermission() {
    const url =  "/Person/get-permission/"
    const res = await axiosClient.get(url);
    // console.log(res.data.code)
    setRole(res.data.permission)
    setMADV(res.data.code)
    console.log("ma don vi")
    console.log(MaDV);
  }
  getPermission();
},[])

//
  return (
    <div className="sidebar" data-image={image} data-color={color}>
      <div
        className="sidebar-background"
        style={{
          backgroundImage: "url(" + image + ")"
        }}
      />
      <div className="sidebar-wrapper">
        <div className="logo d-flex align-items-center justify-content-start">
          <a
            href="https://www.creative-tim.com?ref=lbd-sidebar"
            className="simple-text logo-mini mx-1"
          >
            <div className="logo-img">
              <img src={require("assets/img/Layer2.png")} alt="..." />
            </div>
          </a>
          <a className="simple-text" href="http://www.creative-tim.com">
            <span type="bold">QUẢN LÍ VÀO RA</span>
          </a>
        </div>
        <Nav>
          {routes.map((prop, key) => {
            if (!prop.redirect)
              {
                if(prop.layout === "/admin" && role ===5){
                  return (
                      <li
                        className={
                          prop.upgrade
                            ? "active active-pro"
                            : activeRoute(prop.layout + prop.path)
                        }
                        key={key}
                      >
                        <NavLink
                          to={prop.layout + prop.path}
                          className="nav-link"
                          activeClassName="active"
                        >
                          <i className={prop.icon} />
                          <p>{prop.name}</p>
                        </NavLink>
                      </li>
                  )
                }
                else if(prop.layout==="/vebinh" && role ===4){
                  return (
                    
                    <li
                      className={
                        prop.upgrade
                          ? "active active-pro"
                          : activeRoute(prop.layout + prop.path)
                      }
                      key={key}
                    >
                      <NavLink
                        to={prop.layout + prop.path}
                        className="nav-link"
                        activeClassName="active"
                      >
                        <i className={prop.icon} />
                        <p>{prop.name}</p>
                      </NavLink>
                    </li>
                )
                }
                else if(prop.layout ==="/tieudoan" && role ===3){
                   return (
                    
                    <li
                      className={
                        prop.upgrade
                          ? "active active-pro"
                          : activeRoute(prop.layout + prop.path)
                      }
                      key={key}
                    >
                      <NavLink
                        to={prop.layout + prop.path}
                        className="nav-link"
                        activeClassName="active"
                      >
                        <i className={prop.icon} />
                        <p>{prop.name}</p>
                      </NavLink>
                    </li>
                )
                }
                else if(prop.layout ==="/daidoi" && role ===2){
                  return (
                    
                    <li
                      className={
                        prop.upgrade
                          ? "active active-pro"
                          : activeRoute(prop.layout + prop.path)
                      }
                      key={key}
                    >
                      <NavLink
                        to={prop.layout + prop.path}
                        className="nav-link"
                        activeClassName="active"
                      >
                        <i className={prop.icon} />
                        <p>{prop.name}</p>
                      </NavLink>
                    </li>
                )
                }
                else if(prop.layout ==="/lop" && role ===1){
                  return (
                    
                    <li
                      className={
                        prop.upgrade
                          ? "active active-pro"
                          : activeRoute(prop.layout + prop.path)
                      }
                      key={key}
                    >
                      <NavLink
                        to={prop.layout + prop.path}
                        className="nav-link"
                        activeClassName="active"
                      >
                        <i className={prop.icon} />
                        <p>{prop.name}</p>
                      </NavLink>
                    </li>
                )
                }
              }
            return null;
          })}
        </Nav>
      </div>
    </div>
  );
}

export default Sidebar;
