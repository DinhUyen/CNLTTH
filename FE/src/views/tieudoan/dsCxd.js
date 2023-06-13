import React, { useState, useContext } from "react";
import { useEffect,useRef } from "react";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
import { GlobalState } from "layouts/Slidenav";
import "../../assets/css/btn_vul.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./style.css";
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
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
  const [tt, setTt] = useState();
  const [xetDuyet, setXetDuyet] = useState();
  const [listDSCXD, setlistDSCXD] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const ref = useRef(null)
  const handleChange = (date) => {
    setSelectedDate(date);
  };

  useEffect(() => {
    async function getDSCXD() {
      const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      const res = await axiosClient.get(
        `/Person/get-list-danh-sach-chua-duoc-duyet/?donViID=${id}&timeBetween=${dateString}`
      );
      setlistDSCXD((listDSCXD) => [...res.data]);
    }
    getDSCXD();
  }, [id, selectedDate]);


 async function duyetDSDK(tag){
  const data= {
    STT_dang_ky: STT,
    xet_duyet: xetDuyet
  }
  console.log(data)
  const res = await axiosClient.post("/Person/post-xet-duyet-ra-ngoai/", data)
  if (res.status === 200) {
    tag.innerHTML = "Đã duyệt"
    // alert("Thành công");
    // getDSCXD()
  } else {
    alert("Đã xảy ra lỗi")
  }
 }
 async function khongDuyetDSDK(tag){
  const data= {
    STT_dang_ky: STT,
    xet_duyet: xetDuyet
  }
  console.log(data)
  const res = await axiosClient.post("/Person/post-xet-duyet-ra-ngoai/", data)
  if (res.status === 200) {
    tag.innerHTML = "Không được duyệt"
    // alert("Thành công");
    // getDSCXD()
  } else {
    alert("Đã xảy ra lỗi")
  }
 }
 const handleDuyet = (event,STT) => {
  const tag = event.target.parentNode.parentNode.getElementsByTagName('td')[6];
  console.log(tag);


  // setTt("Đã xét duyệt")
  setXetDuyet(1)
  setSTT(STT)
  confirmAlert({
    message: 'Bạn có chắc chắn DUYỆT?',
    buttons: [
      {
        label: 'Có',
        // onClick: () => {}
        onClick: () => duyetDSDK(tag)
      },
      {
        label: 'Không',
        onClick: () => {}
      }
    ]
  });
};
const handleKhongDuyet = (event,STT) => {
  const tag = event.target.parentNode.parentNode.getElementsByTagName('td')[6];
  console.log(tag);
  console.log(STT)
  setXetDuyet(-1)
  setSTT(STT)
  confirmAlert({
    message: 'Bạn có chắc chắn KHÔNG DUYỆT?',
    buttons: [
      {
        label: 'Có',
        onClick: () => khongDuyetDSDK(tag)
      },
      {
        label: 'Không',
        onClick: () => {}
      }
    ]
  });
};
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
                    {listDSCXD &&
                      listDSCXD.map((item) => {
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
                                onClick={(e) => handleDuyet(e,item.STT)}
                              >
                               Duyệt
                              </Button>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e)=> handleKhongDuyet(e,item.STT)}
                              >
                              Không duyệt
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
      </Container>
    </>
  );
}

export default TableListAdmin;
