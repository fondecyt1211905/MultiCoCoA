import React, { useState, useEffect } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import ActivityService from "../../services/activities.service";
import AnalysisService from "../../services/analysis.service";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Spinner from "react-bootstrap/Spinner";
import { useNavigate } from "react-router-dom";
import Slider from "@mui/material/Slider";

function valuetext(value) {
  return `${value}sec`;
}

const minDistance = 1;

const ModalAnalyzeActivity = (props) => {
  const [activity, setActivity] = useState([]);
  const [spinner, setSpinner] = useState(true);
  let navigate = useNavigate();
  const [rangeminmax, setRange] = React.useState([0, 1]);
  const [max, setMax] = React.useState(1);

  useEffect(() => {
    if (props.activity) {
      ActivityService.get(props.activity)
        .then(({ data }) => {
          //buscar el archivo de mayor duracion
          let max = 0;
          data.files.map((item) => {
            if (item.length > max) {
              max = item.length;
            }
          });
          setMax(max);
          setRange([0, max]);
          setActivity(data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
    // if (props.file) {
    //   ActivityService.get(props.file.split(".")[0])
    //     .then(({ data }) => {
    //       data.files = data.files.filter((item) => item.name == props.file);
    //       setActivity(data.files);
    //     })
    //     .catch((error) => {
    //       console.log(error);
    //     });
    // }
  }, []);

  const handleChange = (event, newValue, activeThumb) => {
    if (!Array.isArray(newValue)) {
      return;
    }

    if (activeThumb === 0) {
      setRange([
        Math.min(newValue[0], rangeminmax[1] - minDistance),
        rangeminmax[1],
      ]);
    } else {
      setRange([
        rangeminmax[0],
        Math.max(newValue[1], rangeminmax[0] + minDistance),
      ]);
    }
  };

  const analizeActivity = () => {
    if (activity.files) {
      setSpinner(false);
      activity.start= rangeminmax[0];
      activity.end= rangeminmax[1];
      AnalysisService.analize(activity)
        .then((result) => {
          console.log(result);
          setSpinner(true);
          alert("Analysis started successfully");
          props.setShowModal(false)
        })
        .catch((err) => {
          setSpinner(true);
          console.log(err);
        });
    }
  };

  const ListElements = () => {
    if (activity.files) {
      return activity.files.map((res, i) => {
        return (
          <ListGroup.Item
            as="li"
            className="d-flex justify-content-between align-items-start"
            obj={res}
            key={i}
          >
            <div className="ms-2 me-auto">{res.filename}</div>
          </ListGroup.Item>
        );
      });
    }

    // if (activity.files.length > 0) {
    //   return activity.files.map((res, i) => {
    //     return (
    //       <ListGroup.Item
    //         as="li"
    //         className="d-flex justify-content-between align-items-start"
    //         obj={res}
    //         key={i}
    //       >
    //         <div className="ms-2 me-auto">{res.filename}</div>
    //       </ListGroup.Item>
    //     );
    //   });
    // }
  };

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <form>
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Confirm Action
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row>
            <Col>
              <h4>This action cannot be interrupted!</h4>
              <p>You are sending the following file(s) for analysis.</p>
            </Col>
          </Row>
          <Row className="p-2">
            <Col>
              <Card>
                <Card.Body>
                  <Card.Title>time interval (Seconds)</Card.Title>
                  <div className="pt-5">
                    <div className="px-4">
                      <Slider
                        getAriaLabel={() => "Minimum distance"}
                        value={rangeminmax}
                        max={max}
                        min={0}
                        onChange={handleChange}
                        getAriaValueText={valuetext}
                        valueLabelDisplay="on"
                        disableSwap
                      />
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row className="p-2">
            <Col>
              <ListGroup as="ol" numbered>
                {ListElements()}
              </ListGroup>
            </Col>
          </Row>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={props.onHide}>
            Close
          </Button>
          <Button
            variant="primary"
            onClick={analizeActivity}
            disabled={!spinner}
          >
            Analyze file(s)
          </Button>
          {!spinner ? (
            <Spinner animation="border" role="status" variant="primary">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          ) : null}
        </Modal.Footer>
      </form>
    </Modal>
  );
};

export default ModalAnalyzeActivity;
