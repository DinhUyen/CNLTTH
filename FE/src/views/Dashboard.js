import React from "react";
import ChartistGraph from "react-chartist";
import Layer2 from "../../src/assets/img/Layer2.png";
import "./dashboard.css";
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
  OverlayTrigger,
  Tooltip,
} from "react-bootstrap";

function Dashboard() {
  return (
    <>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card>
              <Card.Header>
                <Row>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      marginLeft: "20px",
                    }}
                  >
                    <img
                      src={Layer2}
                      style={{
                        width: "80px",
                        height: "80px",
                        marginRight: "10px",
                        backgroundColor: "#F44336",
                        borderRadius: "50%",
                      }}
                    />
                    <Card.Title
                      as="h4"
                      style={{
                        fontSize: "28px",
                        fontWeight: "bold",
                        color: "rgb(0 95 53)",
                        marginLeft: "40px",
                      }}
                    >
                      PHẦN MỀM QUẢN LÝ VÀO RA CHO HỌC VIÊN HỌC VIỆN KỸ THUẬT
                      QUÂN SỰ
                    </Card.Title>
                  </div>
                </Row>
              </Card.Header>
              <Card.Body>
                <div className="typography-line">
                  <p className="bold-text">
                    Theo khảo sát việc đăng ký ra vào bằng sổ sách có hiệu quả
                    không cao, khả năng đối chiếu thông tin thấp, dễ xảy ra sai
                    phạm và khó quản lý.
                  </p>
                  <p className="bold-text">
                    Phần mềm quản lý vào ra cho học viên giúp khắc phục những
                    nhược điểm còn tồn tại theo cách quản lý thủ công. Những ưu
                    điểm của hệ thông bao gồm:
                  </p>
                  <ul>
                    <li>Quản lý chặt chẽ quân số tại đơn vị.</li>
                    <li>
                      Thông tin được lưu trữ trên máy và hạn chế được số người
                      có quyền chỉnh sửa thông tin.
                    </li>
                    <li>
                      Thuận tiện cho việc kiểm tra và xác thực thông tin, hạn
                      chế việc thực hiện thủ công, nâng cao tính chính xác.
                    </li>
                    <li>
                      Thông tin ra ngoài của cá nhân được lưu trữ cụ thể hơn, có
                      thể so khớp với dữ liệu lưu tại đơn vị.
                    </li>
                    <li>
                      Cơ sở để phân tích đánh giá, xem xét vấn đề vi phạm thông
                      thường của học viên khi ra ngoài, đồng thời quản lý tình
                      hình tư tưởng của học viên. Kịp thời điều chỉnh hình thức
                      giáo dục, quản lý cho phù hợp{" "}
                    </li>
                  </ul>
                  <p className="bold-text">
                    Quy trình xử lý như sau:
                  </p>
                  <ul>
                    <li>Học viên có nhu cầu đăng kí ra ngoài, tranh thủ phải đăng kí theo lớp.</li>
                    <li>
                      Đại đội, tiểu đoàn, học viện xem xét có duyệt cho học viên hay không
                    </li>
                    
                    <li>
                      Nếu học viên được duyệt thì trước khi ra cổng phải lên đại đội lấy tích kê hoặc giấy tranh thủ
                    </li>
                    <li>
                      Nếu học viên vi phạm thì lỗi sẽ được vệ binh cập nhật lên hệ thống
                    </li>
                  </ul>
                  <p className="bold-text">
                    Quy định đăng ký ra ngoài, tranh thủ:
                  </p>
                  <ul>
                  <li>Theo quy định, đối với học viên năm nhất, năm 2, năm 3 quân số ra ngoài, tranh thủ không quá 30%; học viên năm tư là không quá 40%; học viên năm cuối là không quá 50%</li>
                    <li>
                      Nếu học viên tranh thủ hoặc ra ngoài vào ngày cuối tuần thì phải được tiểu đoàn duyệt
                    </li>
                    <li>
                      Nếu là học viên miền Nam về tranh thủ thì phải được học viện duyệt
                    </li>
                    <li>
                      Đại đội căn cứ vào rèn luyện thể lực trong tháng, nội vụ vệ sinh và các vi phạm để xem xét có duyệt cho học viên hay không
                    </li>
                    </ul>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Dashboard;
