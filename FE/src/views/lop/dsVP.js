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
  const [STT, setSTT] = useState();
  const [liDo, setLiDo] = useState();
  const [maLoai, setMaLoai] = useState();
  const [soVe, setSoVe] = useState()
  const [listDSVP, setlistDSVP] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showModal, setShowModal] = useState(false);
  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);
  const [TGRa, setTGRa] = useState(new Date());
  const [TGVao, setTGVao] = useState(new Date());

  const handleChange = (date) => {
    setSelectedDate(date);
  };
  const handleTimeVao = (date) => {
    setTGVao(date);
  };
  const handleTimeRa = (date) => {
    setTGRa(date);
  };

  useEffect(() => {
    async function getDSVP() {
      const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      const res = await axiosClient.get(
        "/VeBinh/get-list-loi-vi-pham-/?page=1&size=12"
      );
      console.log(res)
      setlistDSVP((listDSVP) => [...res.data]);
    }
    getDSVP();
  }, [id, selectedDate]);
  function handleAddQDCT(MaHV){
    setShowModal(true);
    setmaHV(MaHV);
  }
  function handleAddQDCT1(){
    const ngayRa = TGRa.getDate();
    const thangRa = TGRa.getMonth() + 1;
    const namRa = TGRa.getFullYear();
    const ngayVao = TGVao.getDate();
    const thangVao = TGVao.getMonth() + 1;
    const namVao = TGVao.getFullYear();
    const timeRa = `${ngayRa}-${thangRa}-${namRa}`;
    const timeVao = `${ngayVao}-${thangVao}-${namVao}`;
    const data ={
      reason: liDo,
      time_start: timeRa,
      time_end: timeVao,
      ma_HV: maHV
    }
    axiosClient.post("/Person/post-them-hoc-vien-cam-trai/", data).then((res)=>{
      if (res.status === 200) {
        alert("Thêm thành công");
        getDSDK()
      } else {
        alert("Đã xảy ra lỗi")
      }
    })
    setShowModal(false);
  }

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

            <div class="form-group">
              <label>Lí do</label>
              <input
                className="form-control url"
                value={liDo}
                onChange={(e) => setLiDo(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Thời gian bắt đầu</label>
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGRa}
                  onChange={handleTimeRa}
                />
            </div>
            <div class="form-group">
              <label>Thời gian kết thúc</label>
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGVao}
                  onChange={handleTimeVao}
                />
            </div>
            <div class="form-group">
              <label>Mã học viên</label>
              <input
                className="form-control url"
                value={maHV}
                onChange={(e) => setLiDo(e.target.value)}
              />
            </div>

          </Form>
        </Modal.Body>
        <Modal.Footer>
        <Button
            variant="secondary"
            onClick={handleAddQDCT1}
            className="btn-table btn-left"
          >
            Thêm DSCT
          </Button>
          <Button onClick={handleClose} variant="secondary" type="submit">
            Hủy
          </Button>
        </Modal.Footer>
      </Modal>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card className="strpied-tabled-with-hover">
              <Card.Header>
                {/* <Col md="3">
                  <div style={{ display: "flex", gap: 12 }}>
                  <p>Ngày trong tuần</p>
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDate}
                    onChange={handleChange}
                  />
                  </div>
                  
                </Col> */}
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">STT</th>
                      <th className="border-0">STT ra ngoài</th>
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Tiểu đoàn</th>
                      <th className="border-0">Đại đội</th>
                      <th className="border-0">Lớp</th>
                      <th className="border-0">Lỗi</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listDSVP &&
                      listDSVP.map((item) => {
                        return (
                          <tr key={item.STT}>
                            <td>{item.STT}</td>
                            <td>{item.STTRaNgoai}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.TenTD}</td>
                            <td>{item.TenDD}</td>
                            <td>{item.TenLop}</td>
                            <td>{item.TenLoi}</td>
                            <td>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => 
                                  handleAddQDCT(
                                     item.MaHV
                                  )}
                              >
                                Thêm QDCT
                              </Button></td>
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
