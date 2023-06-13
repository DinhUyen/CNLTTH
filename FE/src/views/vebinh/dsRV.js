import React, { useState, useContext } from "react";
import { useEffect } from "react";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
import { GlobalState } from "layouts/Slidenav";
import "../../assets/css/btn_vul.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./style.css";
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import Modal from "react-bootstrap/Modal";

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
  Form,
} from "react-bootstrap";

function TableListAdmin() {
  const { id, setId } = useContext(GlobalState);
  const [maHV, setmaHV] = useState();
  const [listDSRV, setlistDSRV] = useState([]);
  const [selectedDateBD, setselectedDateBD] = useState(new Date());
  const [selectedDateKT, setselectedDateKT] = useState(new Date());
  const [showModalAdd, setshowModalAdd] = useState(false);
  const [STTGiayTo, setSTTGiayTo] = useState()
  const handleCloseAdd = () => setshowModalAdd(false);
  const handleShowAdd = () => setshowModalAdd(true);
  const handleChange = (date) => {
    setselectedDateBD(date);
  };
  const handleChangeKT = (date) => {
    setselectedDateKT(date);
  };

  useEffect(() => {
    async function getDSRV() {
      const day = selectedDateBD.getDate();
      const month = selectedDateBD.getMonth() + 1;
      const year = selectedDateBD.getFullYear();
      const dayKT = selectedDateKT.getDate();
      const monthKT = selectedDateKT.getMonth() + 1;
      const yearKT = selectedDateKT.getFullYear();
      const dateStringBD = `${year}-${month}-${day}`;
      const dateStringKT = `${yearKT}-${monthKT}-${dayKT}`;
      const res = await axiosClient.get(
        `/VeBinh/get-list-danh-sach-vao-ra-cong/?page=0&size=12&timeStart=${dateStringBD}&timeEnd=${dateStringKT}`
      );
      console.log(res)
      setlistDSRV((listDSRV) => [...res.data]);
    }
    getDSRV();
  }, [id, selectedDateBD, selectedDateKT]);
  const handleAddDSRV = (e) => {
    console.log("thêm");
    e.preventDefault();
    setshowModalAdd(true);
  };
  const handleAddDSRV1 = (e) => {
    
    const data = {
      STTGiayTo: STTGiayTo
    };
    axiosClient.post("/VeBinh/post-bat-dau-ra-cong/", data).then((res) => {console.log(res)});
    setshowModalAdd(false);
  };
  
  return (
    <>
    <Modal
        style={{ transform: "none" }}
        show={showModalAdd}
        onShow={handleShowAdd}
        onHide={handleCloseAdd}
      >
        <Modal.Header closeButton>
          <Modal.Title>Thêm danh sách ra vào</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <div className="form-group">
              <label>Số giấy tờ</label>
              <div>
              <input
                className="form-control url"
                value={STTGiayTo}
                onChange={(e) => setSTTGiayTo(e.target.value)}
              />
              </div>
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleAddDSRV1}
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
                <Col md="3">
                  <div style={{ display: "flex", gap: 12 }}>
                  <p>Thời gian bắt đầu</p>
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDateBD}
                    onChange={handleChange}
                  />
                  </div>
                  <div style={{ display: "flex", gap: 12 }}>
                  <p>Thời gian kết thúc</p>
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDateKT}
                    onChange={handleChangeKT}
                  />
                  </div>
                  <button
                  type="button"
                  class="btn btn-add-target  btn-table btn-left"
                  onClick={handleAddDSRV}
                >
                  THÊM MỚI
                </button>
                  
                </Col>
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">STT ra ngoài</th>
                      <th className="border-0">STT giấy tờ</th>
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Thời gian ra</th>
                      <th className="border-0">Thời gian vào</th>
                      <th className="border-0">STT đã duyệt</th>
                      <th className="border-0">Số vé</th>
                      <th className="border-0">Loại vé</th>

                    </tr>
                  </thead>
                  <tbody>
                    {listDSRV &&
                      listDSRV.map((item) => {
                        return (
                          <tr key={item.STTRaNgoai}>
                            <td>{item.STTRaNgoai}</td>
                            <td>{item.STTGiayTo}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.TG_Ra}</td>
                            <td>{item.TG_Vao}</td>
                            <td>{item.STTDaDuyet}</td>
                            <td>{item.SoVe}</td>
                            <td>{item.TenLoai}</td>
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
