import React, { useState } from "react";
import { useEffect } from "react";
// import apiAdmin from "../service/Admin/apiAdmin";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";



// react-bootstrap components
import {
  Badge,
  Button,
  Card,
  Navbar,
  Nav,
  Table,
  Container,
  Row,
  Col,
} from "react-bootstrap";

function TableListAdmin() {
  const [listUsers, setlistUsers] = useState([]);
  useEffect(() => {
    async function getItem() {
      const res = await axiosClient.get("users/accepted");
      //console.log(res.data.items);
      // setlistUsers((listUsers) => [...res.data.items, ...listUsers]);
      setlistUsers(res.data.items);
    }
    getItem();

    // getAcc();
    //deleteAcc(id);
  }, []);
  async function deleteItem(id) {
    // console.log('You clicked submit.');
    // console.log(id)
    await axiosClient.delete(`users/${id}/delete`);
      setlistUsers(
        listUsers.filter((user) => {
          return user.id !== id;
        })
      )
  }

  
    // function deleteItem(id) {
    //   console.log(id);
    //   axiosClient.delete(`users/${id}/delete`);
    //   setlistUsers(
    //     listUsers.filter((user) => {
    //       return user.id !== id;
    //     })
    //   )
    // }

    // getAcc();
    //deleteAcc(id);


  // async function deleteAcc(id) {
  //   const respon = await apiAdmin.deleteItem(id);
  //   console.log(respon);
  //   return history.push("/admin/user");
  // }
  const history = useHistory();
  const goDetail = () => history.push("/admin/user");

  //console.log(listUsers);

  // async function deleteItem(id) {
  //   //console.log(id);

  //   const response = await axiosClient.delete(`users/${id}/delete`);
  //   //console.log(response);
  //   history.push("/admin/user");

  // setlistUsers(
  //   listUsers.filter((user) => {
  //     return user.id !== id;
  //   })
  // );
  // history.push("/admin/user");
  // }

  // const addAccount=async(id,email,running,finished,total_alert,total_scan)=>{
  //   let respon=await axiosClient.post('',{
  //     id:id,
  //     email:email,
  //     running:running,
  //     finished:finished,
  //     total_alert:total_alert,
  //     total_scan:total_scan
  //   });
  //   setlistUsers([respon.data.items,...listUsers]);
  // }

  return (
    <>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card className="strpied-tabled-with-hover">
              <Card.Header>
                <Card.Title as="h4">Danh sách người dùng quản trị</Card.Title>
                <p className="card-category">
                  <Button>Add new users</Button>
                </p>
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">ID</th>
                      <th className="border-0">Email</th>
                      <th className="border-0">is_accepted</th>
                      <th className="border-0">running</th>
                      <th className="border-0">finished</th>
                      <th className="border-0">total_alert</th>
                      <th className="border-0">total_scan</th>
                      <th className="border-0">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listUsers &&
                      listUsers.map((item) => {
                        return (
                          <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.email}</td>
                            <td>{String(item.is_accepted)}</td>
                            <td>{item.running}</td>
                            <td>{item.finished}</td>
                            <td>{item.total_scan}</td>
                            <td>{item.total_alert}</td>
                            <td>
                              <Button type="button" onClick={()=>goDetail()}>
                                Detail
                              </Button>
                              <Button onClick={() => deleteItem(item.id)}>
                                Delete
                              </Button>
                              <Button>Update</Button>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default TableListAdmin;
