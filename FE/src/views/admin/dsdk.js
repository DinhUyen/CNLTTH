import React, { useState, useContext } from "react";
import { useEffect } from "react";
// import apiAdmin from "../service/Admin/apiAdmin";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
// import DateTimePicker from 'react-datetime-picker';
import { GlobalState } from "layouts/Slidenav";
import "../../assets/css/btn_vul.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "react-bootstrap/Modal";
import "./style.css";
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import moment from "moment";
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
  Pagination
} from "react-bootstrap";

function TableListAdmin() {
  const { id, setId } = useContext(GlobalState);
  const [maHV, setmaHV] = useState();
  const [STT, setSTT] = useState();
  const [HTRN, setHTRN] = useState(0);
  const [DiaDiem, setDiaDiem] = useState();
  const [TGRa, setTGRa] = useState(new Date());
  const [TGVao, setTGVao] = useState(new Date());
  const [listDSDK, setlistDSDK] = useState([]);
  const [listHTRN, setlistHTRN] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [show, setShow] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [hm, setHm] = useState({
    gioRa: "",
    gioVao: "",
    phutRa: "",
    phutVao: ""
  });

  const handleChange = (date) => {
    setSelectedDate(date);
  };
  const handleTimeVao = (date) => {
    setTGVao(date);
  };
  const handleTimeRa = (date) => {
    setTGRa(date);
  };
  async function getDSDK() {
    const day = selectedDate.getDate();
    const month = selectedDate.getMonth() + 1;
    const year = selectedDate.getFullYear();
    const dateString = `${day}-${month}-${year}`;
    const res = await axiosClient.get(
      `/Person/get-list-dang-ky/?donViID=${id}&timeBetween=${dateString}`
    );
    setlistDSDK((listDSDK) => [...res.data]);
  }
  useEffect(() => {    
    getDSDK();
  }, [id, selectedDate]);

  async function getHTRN() {
    const res = await axiosClient.get("/Person/get-list-hinh-thuc-ra-ngoai");
    setlistHTRN((listHTRN) => [...res.data]);
  }
  function getMaHVShow(maHv) {
    setShow(true);
    setmaHV(maHV);
  }

 async function xoaDSDK(maDK){
  const res = await axiosClient.delete(`/Person/delete-dang-ky/?sttDangKy=${maDK}`)
  // console.log(res.data.status)
  if (res.data.status === true) {
    alert("Xóa thành công");
    getDSDK()
  } else {
    alert("Chỉ được xóa khi chưa xét duyệt")
  }
 }
 const handleDelete = (maDK) => {
  console.log(maDK)
  confirmAlert({
    message: 'Bạn có chắc chắn muốn xóa không?',
    buttons: [
      {
        label: 'Có',
        onClick: () => xoaDSDK(maDK)
      },
      {
        label: 'Không',
        onClick: () => {}
      }
    ]
  });
};
function getThoiGian(ThoiGian){
  const item = { ThoiGian: ThoiGian};
  const momentObj = moment(item.ThoiGian);
  item.ThoiGian= momentObj.format("HH:mm DD-MM-YYYY");
  return item.ThoiGian;
}
  function getTrangThai(TRANGTHAIXD) {
    switch (TRANGTHAIXD) {
      case 1:
        return "Chưa xét duyệt";
      case 2:
        return "Đại đội đã xét duyệt";
      case 3:
        return "Tiểu đoàn đã xét duyệt";
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
function handleEditDSDK (
  STT,
  HTRN,
  DiaDiem
){
    getHTRN() 
    console.log(listHTRN)
    // console.log(HTRN)
    setShowModal(true);
    setSTT(STT)
    setHTRN(HTRN);
    setDiaDiem(DiaDiem);
  };
  const handleEditDSDK1 = (e) => {
    e.preventDefault();
    // console.log(HTRN)
    if (
      TGRa === "" ||
      TGVao === "" ||
      hm.gioRa === "" ||
      hm.gioVao === "" ||
      hm.phutRa === "" ||
      hm.phutVao === "" ||
      DiaDiem === "null"
    ) {
      alert("Nhập thiếu nội dung");
    } else{
    const ngayRa = TGRa.getDate();
    const thangRa = TGRa.getMonth() + 1;
    const namRa = TGRa.getFullYear();
    const ngayVao = TGVao.getDate();
    const thangVao = TGVao.getMonth() + 1;
    const namVao = TGVao.getFullYear();
    const timeRa = `${namRa}-${thangRa}-${ngayRa} ${hm.gioRa}:${hm.phutRa}`;
    const timeVao = `${namVao}-${thangVao}-${ngayVao} ${hm.gioVao}:${hm.phutVao}`;
    const data = {
      STT: STT,
      dia_diem: DiaDiem,
      hinh_thuc_RN: HTRN,
      time_start: timeRa,
      time_end: timeVao,
    };
    axiosClient.put("/Person/put-thay_doi-thong-tin-dang-ky/", data).then((res) => {
      if (res.data.status === true) {
        alert("Chỉnh sửa thành công");
        getDSDK()
      } else {
        alert("Chỉ được thay đổi khi chưa xét duyệt!")
      }
    });
    setShowModal(false);
    }
    
  };
  const paginate = (targets) => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return targets.slice(startIndex, endIndex);
  };

  return (
    <>
      <Modal
        style={{ transform: "none" }}
        show={showModal}
        onShow={handleShow}
        onHide={handleClose}
      >
        <Modal.Header closeButton>
          <Modal.Title>Chỉnh sửa danh sách đăng kí</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <div className="form-group">
              <label>Hình thức ra ngoài</label>
              <div>
                <select
                  class="form-control name-domain"
                  onChange={(event) => setHTRN(event.target.value)}
                >
                  {listHTRN.map((item) => {
                    return (
                      // console.log(item.STT_HTRN),
                      <option value={item.STT}>{item.LOAI}</option>
                    );
                  })}
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Địa điểm</label>
              <input
                className="form-control url"
                value={DiaDiem}
                onChange={(e) => setDiaDiem(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Thời gian ra</label>
              <div style={{ display: "flex", gap: 12 }}>
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGRa}
                  onChange={handleTimeRa}
                />
                <input 
                value={hm.gioRa} 
                placeholder="giờ" 
                style={{ width: 120 }} 
                onChange={(e) => setHm({...hm, gioRa:e.target.value})} />
                <input 
                type = "text"
                value={hm.phutRa} 
                placeholder="phút" 
                style={{ width: 120 }} 
                onChange={(e) => setHm({...hm, phutRa: e.target.value})}/>
                </div>
            </div>
            <div class="form-group">
              <label>Thời gian vào</label>
              <div style={{ display: "flex", gap: 12 }}>
                <DatePicker
                  dateFormat="dd/MM/yyyy"
                  selected={TGVao}
                  onChange={handleTimeVao}
                />
                <input type="text" value={hm.gioVao} placeholder="giờ" style={{ width: 120 }} onChange={(e) => setHm({...hm, gioVao: e.target.value})}/>
                <input type="text" value={hm.phutVao} placeholder="phút" style={{ width: 120 }} onChange={(e) => setHm({...hm, phutVao:e.target.value})}/>
              </div>
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleEditDSDK1}
            className="btn-table btn-left"
          >
            Lưu thay đổi
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
                 <Row>
                 <div style={{ display: "flex", gap: 12 }}>
                  <p style={{display:"inline-block", width:"200px"}}>Ngày trong tuần</p>
                  <DatePicker
                    dateFormat="dd/MM/yyyy"
                    selected={selectedDate}
                    onChange={handleChange}
                  />
                  </div>
                 </Row>
                  
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
                  {paginate(listDSDK).map((item) => {
                        return (
                          <tr key={item.STT}>
                            <td>{item.STT}</td>
                            <td>{item.LOAI}</td>
                            <td>{item.DiaDiem}</td>
                            <td>{getThoiGian(item.ThoiGianDi)}</td>
                            <td>{getThoiGian(item.ThoiGianVe)}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{getTrangThai(item.TRANGTHAIXD)}</td>
                            <td>                            
                              <div style={{ display: "flex", gap: 12, alignItems:"center", flexWrap:"nowrap" }}>
                              <p onClick={(e) =>  handleEditDSDK(
                                    item.STT,
                                    item.STT_HTRN,
                                    item.DiaDiem
                                   )} className="nc-icon nc-tablet-2 text-primary f-15 m-r-5"
                               title="Chỉnh sửa"
                               style={{ cursor: 'pointer', fontWeight: 'bold' }}></p>

                                <p onClick={(e) => handleDelete(item.STT)} className="nc-icon nc-simple-remove text-danger f-15 m-r-5"
                                title="Xóa"
                                style={{ cursor: 'pointer', fontWeight: 'bold'  }}></p>
                              </div>
                              
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </Table>
                <div className="d-flex justify-content-center">
                <Pagination>
                  {currentPage > 1 && (
                    <Pagination.Prev onClick={() => setCurrentPage(currentPage - 1)} className="prev"/>
                  )}
                  {currentPage > 2 && (
                    <Pagination.Ellipsis
                      onClick={() => setCurrentPage(Math.floor(currentPage / 2))}
                    />
                  )}
                  {[...Array(Math.ceil(listDSDK.length / pageSize)).keys()].map(
                    (number) =>
                      Math.abs(currentPage - (number + 1)) <= 2 && (
                        <Pagination.Item
                          key={number}
                          active={currentPage === number + 1}
                          onClick={() => setCurrentPage(number + 1)}
                        >
                          {number + 1}
                        </Pagination.Item>
                      )
                  )}
                  {currentPage <
                    Math.ceil(listDSDK.length / pageSize) - 1 && (
                      <Pagination.Ellipsis
                        onClick={() =>
                          setCurrentPage(
                            Math.ceil(
                              (currentPage +
                                Math.ceil(listDSDK.length / pageSize)) /
                              2
                            )
                          )
                        }
                      />
                    )}
                  {currentPage <
                    Math.ceil(listDSDK.length / pageSize) && (
                      <Pagination.Next onClick={() => setCurrentPage(currentPage + 1)} className="next"/>
                    )}
                </Pagination>
              </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default TableListAdmin;
