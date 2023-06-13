import React, { useState } from "react";
import { useEffect } from "react";
import axiosClient from "service/axiosClient";
import {Link,useLocation} from 'react-router-dom'
import queryString from 'query-string'
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
} from "react-bootstrap";
import { data } from "jquery";

function TableListUser() {
  const { search } = useLocation();
  console.log(search);
  const values = queryString.parse(search)
  console.log(values);
  console.log(values.maHV);
  const [listKQRL, setlistKQRL] = useState([]);
  
  useEffect(() => {
    async function getItem() {
      const url =  `/Person/get-list-ket-qua-ren-luyen-by-id/?page=0&size=12&maHV=${values.maHV}`
      const res = await axiosClient.get(url);

      console.log(res);
      setlistKQRL((listKQRL) => [...res.data]);
      console.log(listKQRL);
    }
    getItem();
  }, [values.maHV]);
 

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
                      <th className="border-0">Mã học viên</th>
                      <th className="border-0">Loại học viên</th>
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Ngày sinh</th>
                      <th className="border-0">Đơn vị</th>
                      <th className="border-0">Thời gian</th>
                      <th className="border-0">Phân loại rèn luyện</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listKQRL &&
                      listKQRL.map((item) => {
                        return (
                          <tr key={item.ThoiGian}>
                            <td>{item.MaHV}</td>
                            <td>{item.PERSONID}</td>
                            <td>{item.HoTen}</td>
                            <td>{item.NgSinh}</td>
                            <td>{item.DonViID}</td>
                            <td>{item.ThoiGian}</td>
                            <td>{item.PhanLoaiRL}</td>
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

export default TableListUser;
