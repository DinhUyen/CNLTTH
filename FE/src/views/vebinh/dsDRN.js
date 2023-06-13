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
  const [listDSDRN, setlistDSDRN] = useState([]);
  const [STTGiayTo, setSTTGiayTo] = useState()

  useEffect(() => {
    async function getDSDRN() {
      const res = await axiosClient.get(
      "/VeBinh/get-list-danh-sach-ra-ngoai-chua-vao/?page=0&size=12"      );
      console.log(res)
      setlistDSDRN((listDSDRN) => [...res.data]);
    }
    getDSDRN();
  }, [id]);

  async function confirm(STTGiayTo){
    const data ={
      STTGiayTo: STTGiayTo
    }
    const res = await axiosClient.post("/VeBinh/post-vao-cong", data)
    if (res.status === 200) {
      alert("Thành công");
      getDSDK()
    } else {
      alert("Đã xảy ra lỗi")
    }
   }
   const handleConfirm = (STTGiayTo) => {
    console.log(STTGiayTo)
    confirmAlert({
      message: 'Xác nhận đã vào?',
      buttons: [
        {
          label: 'Có',
          onClick: () => confirm(STTGiayTo)
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
                      <th className="border-0">STT đã duyệt</th>
                      <th className="border-0">Số vé</th>
                      <th className="border-0">Loại vé</th>

                    </tr>
                  </thead>
                  <tbody>
                    {listDSDRN &&
                      listDSDRN.map((item) => {
                        return (
                          <tr key={item.STTRaNgoai}>
                            <td>{item.STTRaNgoai}</td>
                            <td>{item.STTGiayTo}</td>
                            <td>{item.MaHV}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.TG_Ra}</td>
                            <td>{item.STTDaDuyet}</td>
                            <td>{item.SoVe}</td>
                            <td>{item.TenLoai}</td>
                            <td>
                            <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => handleConfirm(item.STTGiayTo)}
                              >
                                Đã vào
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
