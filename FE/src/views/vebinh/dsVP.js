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
  const [ghiChu, setghiChu] = useState();
  const [maLoai, setMaLoai] = useState();
  const [soVe, setSoVe] = useState()
  const [listDSVP, setlistDSVP] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showModal, setShowModal] = useState(false);
  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);
  const [TGRa, setTGRa] = useState(new Date());
  const [TGVao, setTGVao] = useState(new Date());
  const [listLVP, setlistLVP] = useState([]);
  const [sttRN, setSTTRN] = useState()
  const [loaiLVP, setLoaiLVP] = useState(1)
  const handleChange = (date) => {
    setSelectedDate(date);
  };
  const handleTimeVao = (date) => {
    setTGVao(date);
  };
  const handleTimeRa = (date) => {
    setTGRa(date);
  };
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
  useEffect(() => {
    
    getDSVP();
  }, [id, selectedDate]);
  function handleAddDSVP(){
    getLVP()
    setShowModal(true);
  }
  async function getLVP() {
    const res = await axiosClient.get("VeBinh/get-list-loai-loi_vi_pham/");
    setlistLVP((listLVP) => [...res.data]);
  }
  function handleAddDSVP1(){
    const data ={
      ma_loi_VP: loaiLVP,
      stt_ra_ngoai: sttRN,
      ghi_chu: ghiChu,
    }
    axiosClient.post("/VeBinh/post-loi-vi-pham/", data).then((res)=>{
      if (res.status === 200) {
        alert("Thêm thành công");
        getDSVP()
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

          <div className="form-group">
              <label>Lỗi vi phạm</label>
              <div>
                <select
                  class="form-control name-domain"
                  onChange={(event) => setHTRN(event.target.value)}
                >
                  {listLVP.map((item) => {
                    return (
                      // console.log(item.STT_HTRN),
                      <option value={item.MaLoiVP}>{item.TenLoi}</option>
                    );
                  })}
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Số thứ tự ra ngoài</label>
              <input
                className="form-control url"
                value={sttRN}
                onChange={(e) => setSTTRN(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Ghi chú</label>
              <input
                className="form-control url"
                value={ghiChu}
                onChange={(e) => setghiChu(e.target.value)}
              />
            </div>

          </Form>
        </Modal.Body>
        <Modal.Footer>
        <Button
            variant="secondary"
            onClick={handleAddDSVP1}
            className="btn-table btn-left"
          >
            Thêm DSVP
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
                 <button
                  type="button"
                  class="btn btn-add-target  btn-table btn-left"
                  onClick={handleAddDSVP}
                >
                  THÊM MỚI
                </button>
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
                            <td>{item.GhiChu}</td>
                            {/* <td>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => 
                                  handleAddQDCT(
                                     item.MaHV
                                  )}
                              >
                                Thêm QDCT
                              </Button></td> */}
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
