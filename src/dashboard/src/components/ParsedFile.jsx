import React from "react";
import { Container } from "react-bootstrap";
import Table from "react-bootstrap/Table";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import ErrorsLog from "./ErrorsLog";
import UploadFile from "./UploadFile";

function ParsedFile() {
  return (
    <div>
      <Container>
        <UploadFile />
        
        <Tabs
          defaultActiveKey="profile"
          id="uncontrolled-tab-example"
          className="mb-3"
        >
          
          <Tab eventKey="profile" title="Parsed Data">
            <Table striped className="border">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Carrier Code</th>
                  <th>Flight No</th>
                  <th>Leg Origin</th>
                  <th>Leg Destination</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>EY</td>
                  <td>418</td>
                  <td>AUH</td>
                  <td>KUL</td>
                </tr>
                <tr>
                  <td>1</td>
                  <td>EY</td>
                  <td>418</td>
                  <td>AUH</td>
                  <td>KUL</td>
                </tr>
                <tr>
                  <td>1</td>
                  <td>EY</td>
                  <td>418</td>
                  <td>AUH</td>
                  <td>KUL</td>
                </tr>
                <tr>
                  <td>1</td>
                  <td>EY</td>
                  <td>418</td>
                  <td>AUH</td>
                  <td>KUL</td>
                </tr>
              </tbody>
            </Table>
            <Container>
              <ErrorsLog />
            </Container>
          </Tab>
          <Tab eventKey="json" title="JSON">
            <p>This is a raw data file</p>
          </Tab>
          <Tab eventKey="raw" title="Raw Data">
            <p>This is a raw data file</p>
          </Tab>
          
        </Tabs>
      </Container>
    </div>
  );
}

export default ParsedFile;
