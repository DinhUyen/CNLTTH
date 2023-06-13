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
  const [xetDuyet, setXetDuyet] = useState();
  const [maLoai, setMaLoai] = useState();
  const [soVe, setSoVe] = useState()
  const [listDSDD, setlistDSDD] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showModal, setShowModal] = useState(false);
  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);

  const handleChange = (date) => {
    setSelectedDate(date);
  };

  useEffect(() => {
    async function getDSDD() {
      const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      const res = await axiosClient.get(
        `/Person/get-list-danh-sach-duoc-duyet/?donViID=${id}&timeBetween=${dateString}`
      );
      console.log(res)
      setlistDSDD((listDSDD) => [...res.data]);
    }
    getDSDD();
  }, [id, selectedDate]);
  function handleAddGTRN(STT){
    setShowModal(true);
    setSTT(STT);
  }
  function handleAddGTRN1(){

    const data ={
      ma_loai: maLoai,
      stt_da_duyet: STT,
      so_ve: soVe
    }
    axiosClient.post("/Person/post-tao-giay-to-RN-hoc-vien/", data).then((res)=>{
      if (res.status === 200) {
        alert("Thêm thành công");
        getDSDK()
      } else {
        alert("Đã xảy ra lỗi")
      }
    })
    setShowModal(false);
  }

  function getTrangThai(TRANGTHAIXD) {
    switch (TRANGTHAIXD) {
      case 0:
        return "Chưa xét duyệt";
      case 1:
        return "Đại đội đã xét duyệt";
      case 2:
        return "Tiểu đoàn đã xét duyệt";
      case 3:
      case 4:
      case 5:
        return "Học viện đã xét duyệt";
      case -1:
      case -2:
      case -3:
        return "Không được duyệt";
      default:
        return "Không xác định";
    }
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
          <div className="form-group">
              <label>Loại giấy tờ</label>
              <div>
                <select
                  class="form-control name-domain"
                  onChange={(event) => setMaLoai(event.target.value)}
                >
                  <option value="1">Tích kê điện tử</option>
                  <option value="2">Giấy ra vào</option>
                  <option value="3">Giấy phép</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Số vé</label>
              <input
                className="form-control url"
                value={soVe}
                onChange={(e) => setSoVe(e.target.value)}
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
        <Button
            variant="secondary"
            onClick={handleAddGTRN1}
            className="btn-table btn-left"
          >
            Thêm giấy tờ
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
                <Col md="3">
                  <div style={{ display: "flex", gap: 12 }}>
                  <p>Ngày trong tuần</p>
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDate}
                    onChange={handleChange}
                  />
                  </div>
                  
                </Col>
              </Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">STT</th>
                      <th className="border-0">Hình thức ra ngoài</th>
                      <th className="border-0">Địa điểm</th>
                      <th className="border-0">Thời gian đi</th>
                      <th className="border-0">Thời gian về</th>
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Trạng thái</th>
                      <th className="border-0">Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listDSDD &&
                      listDSDD.map((item) => {
                        return (
                          <tr key={item.STT}>
                            <td>{item.STT}</td>
                            <td>{item.HinhThucRN}</td>
                            <td>{item.DiaDiem}</td>
                            <td>{item.ThoiGianDi}</td>
                            <td>{item.ThoiGianVe}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{getTrangThai(item.TRANGTHAIXD)}</td>
                            <td>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => 
                                  handleAddGTRN(
                                     item.STT                                  )}
                              >
                                Thêm GTRN
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
