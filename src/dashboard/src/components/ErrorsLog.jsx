import React from "react";
import { Container } from "react-bootstrap";

function ErrorsLog() {
  return (
    <div className="mt-top">
      <Container>
        <h1>Problems</h1>
        <div className="shadow border p-3 ">
          <div className="">CMP0.txt:2 Warning: Detected typo 'FJk', fixed to 'FJK'</div>
          <div className="">CMP0.txt:3 Warning: Illegal Character '*', fixed to '.'</div>
          <div className="error-text">CMP0.txt:6 Error: Incorrect file ending</div>
        </div>
      </Container>
    </div>
  );
}

export default ErrorsLog;
