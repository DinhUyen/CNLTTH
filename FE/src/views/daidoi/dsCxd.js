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
import moment from "moment";
import './style.css'
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
  const [tt, setTt] = useState();
  const [xetDuyet, setXetDuyet] = useState();
  const [listDSCXD, setlistDSCXD] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const ref = useRef(null)
  const handleChange = (date) => {
    setSelectedDate(date);
  };

  // useEffect(() => {

  //   async function getDSCXD() {
  //     const day = selectedDate.getDate();
  //     const month = selectedDate.getMonth() + 1;
  //     const year = selectedDate.getFullYear();
  //     const dateString = `${day}-${month}-${year}`;
  //     const res = await axiosClient.get(
  //       `/Person/get-list-danh-sach-chua-duoc-duyet/?donViID=${id}&timeBetween=${dateString}`
  //     );
  //     setlistDSCXD((listDSCXD) => [...res.data]);
  //   }
  //   getDSCXD();
  // }, [id, selectedDate]);
  async function getItem() {
    const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      const res = await axiosClient.get(
        `/Person/get-list-danh-sach-chua-duoc-duyet/?donViID=${id}&timeBetween=${dateString}`
      );
      setlistDSCXD((listDSCXD) => [...res.data]);
  }  
  useEffect(() => {
    getItem();
  }, [id, selectedDate]);
  const paginate = (targets) => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return targets.slice(startIndex, endIndex);
  };
 async function duyetDSDK(tag){
  const data= {
    STT_dang_ky: STT,
    xet_duyet: xetDuyet
  }
  console.log(data)
  const res = await axiosClient.post("/Person/post-xet-duyet-ra-ngoai/", data)
  if (res.status === 200) {
    // tag.innerHTML = "Đã duyệt"
    alert("Thành công");
    getItem()  }
  else {
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
    // tag.innerHTML = "Không được duyệt"
    alert("Thành công");
    getItem()
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
      case -2:
      case -3:
      case -5:
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
                <Col >
                  <Row>
                  <div style={{ display: "flex", gap: 12, alignItems:"center", flexWrap:"nowrap" }}>
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
                      {/* <th className="border-0">Thao tác</th> */}
                    </tr>
                  </thead>
                  <tbody>
                  {paginate(listDSCXD).map((item) => {
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
                              {/* <Button
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
                              </Button> */}
                              <div  style={{ display: "flex", gap: 12, alignItems:"center", flexWrap:"nowrap" }}>
                              <p onClick={(e) => handleDuyet(e,item.STT)} className="nc-icon nc-check-2 text-primary f-15 m-r-5"
                               title="Duyệt"
                               style={{ cursor: 'pointer', fontWeight: 'bold'  }}></p>
                               <p onClick={(e) => handleKhongDuyet(e,item.STT)} className="nc-icon nc-simple-remove text-danger f-15 m-r-5"
                               title="Không duyệt"
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
                  {[...Array(Math.ceil(listDSCXD.length / pageSize)).keys()].map(
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
                    Math.ceil(listDSCXD.length / pageSize) - 1 && (
                      <Pagination.Ellipsis
                        onClick={() =>
                          setCurrentPage(
                            Math.ceil(
                              (currentPage +
                                Math.ceil(listDSCXD.length / pageSize)) /
                              2
                            )
                          )
                        }
                      />
                    )}
                  {currentPage <
                    Math.ceil(listDSCXD.length / pageSize) && (
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
