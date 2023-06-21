import "./App.css";
import React from "react";
import NavbarComp from "./components/NavbarComp";
import UploadFile from "./components/UploadFile";
import ParsedFile from "./components/ParsedFile";
import History from "./components/History";
import { Col, Row } from "react-bootstrap";
import ErrorsLog from "./components/ErrorsLog";

function App() {
  return (
    <div className="app">
      <NavbarComp />
      <Row>
        <Col md={3}>
          <History />
        </Col>
        <Col md={9}>
          <ParsedFile />
        </Col>
      </Row>
    </div>
  );
}

export default App;
