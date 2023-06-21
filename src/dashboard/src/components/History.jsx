import React from "react";
import { Container } from "react-bootstrap";
import ListGroup from "react-bootstrap/ListGroup";

function History() {
  return (
    <div>
      <Container>
        <h3>History</h3>
        <ListGroup>
          <ListGroup.Item action variant="danger" className="my-2">
            CPM0.txt
          </ListGroup.Item>
          <ListGroup.Item action variant="danger" className="my-2">
            CPM1.txt
          </ListGroup.Item>
          <ListGroup.Item action variant="danger" className="my-2">
            CPM2.txt
          </ListGroup.Item>
          <ListGroup.Item action variant="danger" className="my-2">
            CPM3.txt
          </ListGroup.Item>
          <ListGroup.Item action variant="danger" className="my-2">
            CPM4.txt
          </ListGroup.Item>
        </ListGroup>
      </Container>
    </div>
  );
}

export default History;
