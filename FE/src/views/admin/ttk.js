import React, { useState } from "react";
import { useEffect } from "react";
// import apiAdmin from "../service/Admin/apiAdmin";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import "../../assets/css/btn_vul.css";
import "./style.css";

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
  Form
} from "react-bootstrap";

function TableListAdmin() {
  const [listAccount, setlistAccount] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);
  const [personID, setPersonID] =useState()
  const [username, setUsername] = useState()
  const [roleID, setRoleID] = useState("1")
  const [showAdd, setshowAdd] = useState(false);
  const handleCloseAdd = () => setshowAdd(false);
  const handleShowAdd = () => setshowAdd(true);
  async function getItem() {
    const res = await axiosClient.get("/Person/get-list-account/?page=1&size=12");

    setlistAccount((listAccount) => [...res.data]);
  }
  useEffect(() => {
   
    getItem();

  }, []);
  function setRole(username){
    setShowModal(true);
    setUsername(username);
  }
  function setRole1(){
console.log(roleID)
const parsedRoleID = parseInt(roleID);
const parsedPersonID = parseInt(personID);
    const data ={
      username: username,
      roleID: parsedRoleID,
      personID: parsedPersonID
      
    }
    axiosClient.post("/account/setRoleUser", data).then((res)=>{
      if (res.status === 200) {
        alert("Thêm thành công");
        getItem()
      } else {
        alert("Đã xảy ra lỗi")
      }
    })
    setShowModal(false);
  }
  function getRole(RoleID) {
    switch (RoleID) {
      case 1:
        return "Lớp";
      case 2:
        return "Đại đội";
      case 3:
        return "Tiểu đoàn";
      case 4:
        return "Vệ binh"
      case 5:
        return "Học viện";
      default:
        return "Không xác định";
    }
  }
  const handleAddTK = (e => {
    console.log("thêm");
    e.preventDefault();
    getItem();
    setshowAdd(true);
  });
  const handleAddTK1 = (e => {
    console.log("thêm");
    e.preventDefault();
    getItem();
    setshowAdd(true);
  });
  
  

  return (
    <>
        <Modal
        style={{ transform: "none" }}
        show={showModal}
        onShow={handleShow}
        onHide={handleClose}
      >
        <Modal.Header closeButton>
        </Modal.Header>
        <Modal.Body>
          <Form>
          <div className="form-group">
              <label>Set roleID</label>
              <div>
                <select
                  class="form-control name-domain"
                  onChange={(event) => setRoleID(event.target.value)}
                >
                  <option value="1">Quyền của lớp</option>
                  <option value="2">Quyền của đại đội</option>
                  <option value="3">Quyền của tiểu đoàn</option>
                  <option value="4">Quyền của vệ binh</option>
                  <option value="5">Quyền của học viện</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Person ID</label>
              <input
                className="form-control url"
                value={personID}
                onChange={(e) => setPersonID(e.target.value)}
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
        <Button
            variant="secondary"
            onClick={setRole1}
            className="btn-table btn-left"
          >
            Set Role
          </Button>
          <Button onClick={handleClose} variant="secondary" type="submit">
            Hủy
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal
        style={{ transform: "none" }}
        show={showAdd}
        onShow={handleShowAdd}
        onHide={handleCloseAdd}
      >
        <Modal.Header closeButton>
          <Modal.Title>Thêm người dùng</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            {/* <div className="form-group">
              <label>Hình thức ra ngoài</label>
              <div>
                <select
                  class="form-control name-domain"
                  onChange={(event) => setHTRN(event.target.value)}
                >
                  {listHTRN.map((item) => {
                    return <option value={item.STT}>{item.LOAI}</option>;
                  })}
                </select>
              </div> */}
            {/* </div> */}
            <div class="form-group">
              <label>Tên đăng nhập</label>
              <input
                className="form-control url"
              />
            </div>
            <div class="form-group">
              <label>Mật khẩu</label>
              <input
                type="password"
                className="form-control url"
              />
            </div>
            <div class="form-group">
              <label>Nhập lại Mật khẩu</label>
              <input
                type="password"
                className="form-control url"
              />
            </div>

            <div class="form-group">
              <label>Mã người dùng</label>
              <input
                className="form-control url"
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleAddTK1}
            className="btn-table btn-left"
          >
            Thêm
          </Button>
          <Button onClick={handleCloseAdd} variant="secondary" type="submit">
            Đóng
          </Button>
        </Modal.Footer>
      </Modal>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card className="strpied-tabled-with-hover">
              <Card.Header>
                <Card.Title as="h4">Danh sách người dùng</Card.Title>
                {/* <p className="card-category"> */}
                  <Button
                    type="button"
                    onClick={handleAddTK}
                    class="btn btn-add-target  btn-table btn-left"
                  >Add new users</Button>
                {/* </p> */}
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">ID</th>
                      <th className="border-0">Tên đăng nhập</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Cấp bậc</th>
                      <th className="border-0">Chức Vụ</th>                     
                      <th className="border-0">Tiểu đoàn</th>
                      <th className="border-0">Đại đội</th>
                      <th className="border-0">Lớp</th>
                      <th className="border-0">Quyền</th>
                      <th className="border-0">Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listAccount &&
                      listAccount.map((item) => {
                        return (
                          <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.username}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.CapBac}</td>
                            <td>{item.ChucVu}</td>                                                      
                            <td>{item.TenTD}</td>
                            <td>{item.TenDD}</td>
                            <td>{item.TenLop}</td>
                            <td>{getRole(item.roleID)}</td> 
                            <td>
                              {/* <Button onClick={() => setRole(item.username)}>
                                Set Role
                              </Button> */}
                            
                              <p onClick={(e) => setRole(item.username)} className="nc-icon   nc-settings-gear-64 text-primary f-15 m-r-5"
                                title="Đặt quyền cho người dùng"
                                style={{ cursor: 'pointer', fontWeight: 'bold'  }}></p>

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
