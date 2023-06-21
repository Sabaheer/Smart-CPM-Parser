import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

function UploadFile() {
  return (
    <Container>
      <Form>
        <Row className="d-flex align-items-center">
          <Col md={5}>
            <Form.Group className="mb-3 mt-3" controlId="formBasicEmail">
              <Form.Label>Upload file</Form.Label>
              <Form.Control
                type="file"
                placeholder="Your file name"
                accept=".txt"
              />
              <Form.Text className="text-muted">
                
              </Form.Text>
            </Form.Group>
          </Col>
          <Col md={5}>
            <Button variant="primary" type="submit" className="mt-3 w-25 ">
              Submit
            </Button>
          </Col>
        </Row>
      </Form>
    </Container>
  );
}

export default UploadFile;
