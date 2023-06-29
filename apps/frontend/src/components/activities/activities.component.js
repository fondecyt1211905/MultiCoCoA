import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ActivityService from "../../services/activities.service";
import ActivityRow from "./activityRow.component";

export default function Activities() {
  const [activities, setActivities] = useState([]);
  let navigate = useNavigate();

  useEffect(() => {
    ActivityService.getAll()
      .then(({ data }) => {
        //console.log(data)
        setActivities(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const newActivity = () => {
    navigate("/create-activity/");
  };

  const DataElements = () => {
    return activities.map((res, i) => {
      //console.log(res)
      return <ActivityRow obj={res} key={i} />;
    });
  };
  return (
    <>
      <Container fluid="md text-start">
        <Row className="p-2">
          <Col>
            <Card>
              <Card.Header>Activities</Card.Header>
              <Card.Body>
                <Card.Title>Activities list:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={newActivity}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> New activity</i>
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
