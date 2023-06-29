import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Alert from "react-bootstrap/Alert";
import FormGroup from "react-bootstrap/FormGroup";
import Form from "react-bootstrap/Form";
import Spinner from "react-bootstrap/Spinner";
import ActivityService from "../../services/activities.service";
//import axios from "axios";

export default function CreateActivities() {
  const [name, setName] = useState("");
  const [filea, setFilea] = useState(undefined);
  const [filev, setFilev] = useState(undefined);
  const [alert, setAlert] = useState({
    menssage: "",
    variant: "primary",
    show: false,
  });
  const [spinner, setSpinner] = useState(true);
  let navigate = useNavigate();

  const handleText = (event) => {
    setName(event.target.value);
  };

  const handleFileA = (event) => {
    setFilea(event.target.files[0]);
  };

  const handleFileV = (event) => {
    setFilev(event.target.files[0]);
  };

  const activitiesList = () => {
    navigate("/activities");
  };

  const upload = (event) => {
    event.preventDefault();
    setSpinner(false);
    let formData = new FormData();
    formData.append("file_audio", filea);
    formData.append("file_video", filev);
    formData.append("activities", name);

    ActivityService.create(formData)
      .then((result) => {
        setAlert({
          variant: "success ",
          show: true,
          menssage: result.data.message,
        });
        setSpinner(true);
        setName("");
      })
      .catch((error) => {
        console.log(error)
        setAlert({
          variant: "danger ",
          show: true,
          menssage: error.response.data.error,
        });
        setSpinner(true);
        setName("");
      });
  };

  return (
    <>
      <Container fluid="md text-start">
        <Row className="p-2">
          <Col>
            <Card>
              <Card.Header>New activity</Card.Header>
              <Card.Body>
                <Card.Title>Create new activity:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={activitiesList}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> Activities list</i>
                  </Button>
                </ButtonGroup>
                <Alert variant={alert.variant} show={alert.show}>
                  {alert.menssage}
                </Alert>
                <div className="form-wrapper">
                  <form>
                    <FormGroup className="p-2">
                      <Form.Control
                        type="text"
                        value={name}
                        onChange={handleText}
                        placeholder="Name"
                      ></Form.Control>
                    </FormGroup>
                    <FormGroup className="p-2">
                      <Form.Control
                        type="file"
                        accept="audio/wav"
                        onChange={handleFileA}
                      ></Form.Control>
                    </FormGroup>
                    <FormGroup className="p-2">
                      <Form.Control
                        type="file"
                        accept="video/mp4"
                        onChange={handleFileV}
                      ></Form.Control>
                    </FormGroup>
                    <FormGroup className="p-2">
                      <Button
                        variant="primary"
                        onClick={upload}
                        disabled={!spinner}
                      >
                        Upload File
                      </Button>
                    </FormGroup>
                    {!spinner ? (
                      <FormGroup className="p-2">
                        <Spinner
                          animation="border"
                          role="status"
                          variant="primary"
                        >
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      </FormGroup>
                    ) : null}
                  </form>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}
