import React from "react";
import { Button } from "react-bootstrap";
import ListGroup from "react-bootstrap/ListGroup";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import IndicatorService from "../../services/indicators.service";

const IndicatorRow = (props) => {
  const row = props.obj;

  const download = () => {
    IndicatorService.getcsv(props.obj, props.id_process)
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `${props.obj}-${props.id_process}.csv`);
        document.body.appendChild(link);
        link.click();
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <ListGroup.Item
      as="li"
      className="d-flex justify-content-between align-items-center"
    >
      <div className="ms-6 me-auto p-2">
        <div className="fw-bold">{props.obj}</div>
      </div>
      <ButtonGroup aria-label="actions">
        <Button onClick={download} variant="outline-primary">
          <i className="bi bi-cloud-arrow-down"> Download</i>
        </Button>
      </ButtonGroup>
    </ListGroup.Item>
  );
};

export default IndicatorRow;
