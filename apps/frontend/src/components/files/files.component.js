import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import ActivityService from "../../services/activities.service";
import FileRow from "./fileRow.component";

export default function Files(props) {
  let { name } = useParams();
  const [files, setActivities] = useState([]);

  useEffect(() => {
    ActivityService.get(name)
      .then(({ data }) => {
        //console.log(data);
        setActivities(data.files);
        //console.log(files);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const upload = () => {
    //upload file
  };

  const DataElements = () => {
    return files.map((res, i) => {
      return <FileRow obj={res} key={i} />;
    });
  };

  return (
    <>
      <Container fluid="md text-start">
        <Row className="my-2">
          <Col>
            <Card>
              <Card.Header>Files</Card.Header>
              <Card.Body>
                <Card.Title>Activity: {name}</Card.Title>
                <Card.Subtitle>File List:</Card.Subtitle>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={upload}
                    variant="outline-primary"
                  >
                    <i className="bi bi-cloud-arrow-up"> Upload file</i>
                  </Button>
                </ButtonGroup>
                <ListGroup as="ol" numbered>
                  {DataElements()}
                </ListGroup>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}
