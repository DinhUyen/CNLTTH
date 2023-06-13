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
  const [listGTRV, setlistGTRV] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());

  const handleChange = (date) => {
    setSelectedDate(date);
  };

  useEffect(() => {
    async function getGTRV() {
      const day = selectedDate.getDate();
      const month = selectedDate.getMonth() + 1;
      const year = selectedDate.getFullYear();
      const dateString = `${day}-${month}-${year}`;
      const res = await axiosClient.get(
        `/Person/get-list-giay-to-RN-hoc-vien/?donViID=${id}&timeBetween=${dateString}&page=1&size=12`
      );
      console.log(res)
      setlistGTRV((listGTRV) => [...res.data]);
    }
    getGTRV();
  }, [id, selectedDate]);
  async function xoaGTRV(STT){
    const res = await axiosClient.delete(`/Person/delete-giay-to-RN-hoc-vien/?sttGiayToRN=${STT}`)
    if (res.status === 200) {
      alert("Xóa thành công");
      getDSDK()
    } else {
      alert("Đã xảy ra lỗi")
    }
   }
   const handleDelete = (STT) => {
    console.log(STT)
    confirmAlert({
      message: 'Bạn có chắc chắn muốn xóa không?',
      buttons: [
        {
          label: 'Có',
          onClick: () => xoaGTRV(STT)
        },
        {
          label: 'Không',
          onClick: () => {}
        }
      ]
    });
  };

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
                      <th className="border-0">Số vé</th>
                      <th className="border-0">Thời gian đi</th>
                      <th className="border-0">Thời gian về</th>
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Lớp</th>
                      <th className="border-0">Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listGTRV&&
                      listGTRV.map((item) => {
                        return (
                          <tr key={item.STTGiayTo}>
                            <td>{item.STTGiayTo}</td>
                            <td>{item.SoVe}</td>
                            <td>{item.ThoiGianDi}</td>
                            <td>{item.ThoiGianVe}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.TenLop}</td>
                            <td>
                            <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => handleDelete(item.STTGiayTo)}
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
      </Container>
    </>
  );
}

export default TableListAdmin;
