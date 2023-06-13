import React, { useState, useContext } from "react";
import { useEffect } from "react";
// import apiAdmin from "../service/Admin/apiAdmin";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
import { GlobalState } from "layouts/Slidenav";
import { Pagination } from "@mui/material";
import Modal from "react-bootstrap/Modal";
import "../assets/css/btn_vul.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

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
  const [maHV, setMaHV] = useState();
  const [liDo, setLiDo] = useState();
  const [TGBD, setTGBD] = useState(new Date());
  const [TGKT, setTGKT] = useState(new Date());
  const [listDSCT, setlistDSCT] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [show, setShow] = useState(false);
  const [showModalAdd, setshowModalAdd] = useState(false);
  const handleCloseAdd = () => setshowModalAdd(false);
  const handleShowAdd = () => setshowModalAdd(true);
  const handleChange = (date) => {
    setSelectedDate(date);
  };
  const handleTimeBD = (date) => {
    setTGBD(date);
  };
  const handleTimeKT = (date) => {
    setTGKT(date);
  };
  useEffect(() => {
    async function getDSCT() {
      const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      console.log(dateString);
      const res = await axiosClient.get(
        `/Person/get-list-cam-trai-in-week/?donViID=${id}&timeBetween=${dateString}`
      );
      console.log(res);
      setlistDSCT((listDSCT) => [...res.data]);
      console.log(listDSCT);
    }
    getDSCT();
  }, [id, selectedDate]);
  function getMaHV(maHv) {
    setShow(true);
    setMaHV(maHV);
  }
 
  const handleAddDSCT = (e) => {
    console.log("thêm");
    e.preventDefault();
    setshowModalAdd(true);
  };
  const handleAddDSCT1 = (e) => {
    e.preventDefault();
    if (
      TGBD === "" ||
      TGKT === "" ||
      maHV === "" ||
      liDo === ""
    ) {
      alert("Nhập thiếu nội dung");
    const ngayBD = TGBD.getDate();
    const thangBD = TGBD.getMonth() + 1;
    const namBD = TGBD.getFullYear();
    const ngayKT = TGKT.getDate();
    const thangKT = TGKT.getMonth() + 1;
    const namKT = TGKT.getFullYear();
    const timeBD = `${namBD}-${thangBD}-${ngayBD}`;
    const timeKT = `${namKT}-${thangKT}-${ngayKT}`;
    console.log(liDo)
    console.log(timeBD)
    console.log(timeKT)
    console.log(maHV)
    const data = {
      reason: liDo,
      time_start: timeBD,
      time_end: timeKT,
      ma_HV: maHV,
    };
    axiosClient.post("/Person/post-them-hoc-vien-cam-trai/", data).then((res) => {console.log(res)});
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
          <Modal.Title>Thêm danh sách cấm trại</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <div className="form-group">
              <label>Mã học viên</label>
              <div>
              <input
                className="form-control url"
                value={maHV}
                onChange={(e) => setMaHV(e.target.value)}
              />
              </div>
            </div>
            <div class="form-group">
              <label>Thời gian bắt đầu</label>
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGBD}
                  onChange={handleTimeBD}
                  />
            </div>
            <div class="form-group">
              <label>Thời gian kết thúc</label>
            
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGKT}
                  onChange={handleTimeKT}
                  />
            </div>
            <div class="form-group">
              <label>Lí do</label>
              <input
                className="form-control url"
                value={liDo}
                onChange={(e) => setLiDo(e.target.value)}
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleAddDSCT1}
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
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDate}
                    onChange={handleChange}
                  />
                </Col>
                <button
                  type="button"
                  class="btn btn-add-target  btn-table btn-left"
                  onClick={handleAddDSCT}
                >
                  THÊM MỚI
                </button>
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                <thead>
                    <tr>
                      <th className="border-0">STT</th>
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Thời gian bắt đầu</th>
                      <th className="border-0">Thời gian kết thúc</th>
                      <th className="border-0">Lí do</th>
                    </tr>
                  </thead>
                  <tbody>
                  {listDSCT &&
                      listDSCT.map((item) => {
                        return (
                          <tr key={item.STT}>
                            <td>{item.STT}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.TG_BatDau}</td>
                            <td>{item.TG_KetThuc}</td>
                            <td>{item.LIDO}</td>
                            <td>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => getMaHV(item.id)}
                              >
                                Chỉnh sửa
                              </Button>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => getMaHV(item.id)}
                              >
                                Xóa
                              </Button>
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
            <Pagination count={10} variant="outlined" />
          </Container>
        </>
      );
    }
  }
export default TableListAdmin;
    
	