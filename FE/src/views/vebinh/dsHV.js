import React, { useState, useContext } from "react";
import { useEffect } from "react";
// import apiAdmin from "../service/Admin/apiAdmin";
import axiosClient from "service/axiosClient";
import { useHistory } from "react-router-dom";
import { GlobalState } from "layouts/Slidenav";
import { Pagination } from "@mui/material";
import Modal from "react-bootstrap/Modal";
import "../../assets/css/btn_vul.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Link } from "react-router-dom";
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
  const [hoTen, setHoTen] = useState();
  const [loaiHV, setLoaiHV] = useState();
  const [ngaySinh, setNgaySinh] = useState();
  const [capBac, setCapBac] = useState();
  const [chucVu, setChucVu] = useState();
  const [daiDoi, setDaiDoi] = useState();
  const [lop, setLop] = useState();
  const [queQuan, setQueQuan] = useState();

  const [HTRN, setHTRN] = useState(0);
  const [DiaDiem, setDiaDiem] = useState();
  const [TGRa, setTGRa] = useState(new Date());
  const [TGVao, setTGVao] = useState(new Date());
  const [listHV, setlistHV] = useState([]);
  const [show, setShow] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleCloseAdd = () => setShowAdd(false);
  const handleShowAdd = () => setShowAdd(true);
  const [hm, setHm] = useState({
    gioRa: "",
    gioVao: "",
    phutRa: "",
    phutVao: "",
  });
  const handleTimeVao = (date) => {
    setTGVao(date);
  };
  const handleTimeRa = (date) => {
    setTGRa(date);
  };
  useEffect(() => {
    async function getItem() {
      const res = await axiosClient.get(
        `/Person/get-list-hoc-vien/?page=0&size=12&donViID=${id}`
      );
      console.log(res);
      setlistHV((listHV) => [...res.data]);
    }
    getItem();
  }, [id]);

  const handleAddDSDK = (e, maHV) => {
    console.log("thêm");
    e.preventDefault();
    setmaHV(maHV);
    setShowAdd(true);
  };
  const handleAddDSDK1 = (e) => {
    e.preventDefault();
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
    } else {
      const ngayRa = TGRa.getDate();
      const thangRa = TGRa.getMonth() + 1;
      const namRa = TGRa.getFullYear();
      const ngayVao = TGVao.getDate();
      const thangVao = TGVao.getMonth() + 1;
      const namVao = TGVao.getFullYear();
      const timeRa = `${namRa}-${thangRa}-${ngayRa} ${hm.gioRa}:${hm.phutRa}`;
      const timeVao = `${namVao}-${thangVao}-${ngayVao} ${hm.gioVao}:${hm.phutVao}`;

      const data = {
        hinh_thuc_RN: parseInt(HTRN, 10),
        dia_diem: DiaDiem,
        time_start: timeRa,
        time_end: timeVao,
        ma_HV: maHV,
      };
      axiosClient.post("/Person/post-dang-ky-ra-ngoai/", data).then((res) => {
        // console.log(res.status)
        if (res.status === 200) {
          alert("Thêm thành công");
        } else {
          if (res.status === 500) alert("Thiếu nội dung");
        }
      });
      setShowAdd(false);
    }
  };
  function getTTHV(
    maHv,
    hoTen,
    loaiHV,
    ngaySinh,
    capBac,
    chucVu,
    daiDoi,
    lop,
    queQuan
  ) {
    setShow(true);
    setmaHV(maHv);
    setHoTen(hoTen);
    setLoaiHV(loaiHV);
    setNgaySinh(ngaySinh);
    setCapBac(capBac);
    setChucVu(chucVu);
    setDaiDoi(daiDoi);
    setLop(lop);
    setQueQuan(queQuan);
  }
  return (
    <>
      <Modal
        style={{ transform: "none" }}
        show={showAdd}
        onShow={handleShowAdd}
        onHide={handleCloseAdd}
      >
        <Modal.Header closeButton>
          <Modal.Title>Thêm danh sách đăng kí</Modal.Title>
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
                  <option value="0">Tranh thủ</option>
                  <option value="1">Ra ngoài</option>
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
                  onChange={(e) => setHm({ ...hm, gioRa: e.target.value })}
                />
                <input
                  type="text"
                  value={hm.phutRa}
                  placeholder="phút"
                  style={{ width: 120 }}
                  onChange={(e) => setHm({ ...hm, phutRa: e.target.value })}
                />
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
                <input
                  type="text"
                  value={hm.gioVao}
                  placeholder="giờ"
                  style={{ width: 120 }}
                  onChange={(e) => setHm({ ...hm, gioVao: e.target.value })}
                />
                <input
                  type="text"
                  value={hm.phutVao}
                  placeholder="phút"
                  style={{ width: 120 }}
                  onChange={(e) => setHm({ ...hm, phutVao: e.target.value })}
                />
              </div>
            </div>
            <div class="form-group">
              <label>Mã học viên</label>
              <input
                className="form-control url"
                value={maHV}
                onChange={(e) => setmaHV(e.target.value)}
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleAddDSDK1}
            className="btn-table btn-left"
          >
            Thêm
          </Button>
          <Button onClick={handleCloseAdd} variant="secondary" type="submit">
            Đóng
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Chi tiết học viên</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <div className="form-group">
              <label>Mã học viên</label>
              <input
                disabled
                className="form-control url"
                value={maHV}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Loại học viên</label>
              <input
                disabled
                className="form-control url"
                value={loaiHV}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

            <div class="form-group">
              <label>Họ tên</label>
              <input
                disabled
                className="form-control url"
                value={hoTen}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Ngày sinh</label>
              <input
                disabled
                className="form-control url"
                value={ngaySinh}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Cấp bậc</label>
              <input
                disabled
                className="form-control url"
                value={capBac}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Chức vụ</label>
              <input
                disabled
                className="form-control url"
                value={chucVu}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Đại đội</label>
              <input
                disabled
                className="form-control url"
                value={daiDoi}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Lớp</label>
              <input
                disabled
                className="form-control url"
                value={lop}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div class="form-group">
              <label>Quê quán</label>
              <input
                disabled
                className="form-control url"
                value={queQuan}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleClose}
            className="btn-table btn-left"
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card className="strpied-tabled-with-hover">
              <Card.Header></Card.Header>
              <Card.Body className="table-full-width table-responsive px-0">
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">Mã học viên</th>
                      {/* <th className="border-0">Loại học viên</th> */}
                      <th className="border-0">Họ tên</th>
                      <th className="border-0">Ngày sinh</th>
                      {/* <th className="border-0">Cấp bậc</th> */}
                      {/* <th className="border-0">Chức vụ</th> */}
                      <th className="border-0">Đại đội</th>
                      <th className="border-0">Lớp</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listHV &&
                      listHV.map((item) => {
                        return (
                          <tr key={item.MaHV}>
                            <td>{item.MaHV}</td>
                            {/* <td>{item.TENLOAI}</td> */}
                            {/* <td>{item.PERSONID}</td> */}
                            <td>{item.HoTen}</td>
                            <td>{item.NgSinh}</td>
                            {/* <td>{item.CapBac}</td> */}
                            {/* <td>{item.ChucVu}</td> */}
                            <td>{item.TenDD}</td>
                            <td>{item.TenLop}</td>
                            <td>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) =>
                                  getTTHV(
                                    item.MaHV,
                                    item.HoTen,
                                    item.TENLOAI,
                                    item.NgSinh,
                                    item.CapBac,
                                    item.ChucVu,
                                    item.TenDD,
                                    item.TenLop,
                                    item.QueQuan
                                  )
                                }
                              >
                                Chi tiết
                              </Button>
                              <Button
                                type="button"
                                className="btn-table btn-left"
                                onClick={(e) => handleAddDSDK(e, item.MaHV)}
                              >
                                Thêm DSDK
                              </Button>
                              <Link to={`/admin/kqrl?maHV=${item.MaHV}`}> 
                              <Button type="button" 
                              className="btn-table btn-left" 
                              > 
                              KQRL
                              </Button>
                            </Link>
                             
                            </td>
                            {/* <td>
                              <Button type="button" onClick={()=>goDetail()}>
                                Detail
                              </Button>
                              <Button onClick={() => deleteItem(item.id)}>
                                Delete
                              </Button>
                              <Button>Update</Button>
                            </td> */}
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
export default TableListAdmin;
