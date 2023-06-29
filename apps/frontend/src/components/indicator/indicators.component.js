import React, { useState, useEffect} from "react";
import { useParams} from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import IndicatorRow from "./indicatorRow.component";
import analysisService from "../../services/analysis.service";

export default function Results(props){
    let { id_analysis } = useParams();
    const [indicators, setIndicators] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            analysisService.get(id_analysis).then(({ data }) => {
                setIndicators(data.indicators);
            }).catch((error) => {
                console.log(error);
            });
        }
        
        fetchData()

        const intervalId = setInterval(() => {
            console.log("update data")
            fetchData();
        }, 50000); // 5 minutes in milliseconds
      
        return () => clearInterval(intervalId);

    }, []);

    const DataElements = () => {
        if (indicators) {
            return indicators.map((res, i) => {
                return <IndicatorRow obj={res} key={i} id_process={id_analysis}/>;
            });
        }
    };

    return (
        <>
            <Container fluid="md text-start">
                <Row className="p-2">
                    <Col>
                        <Card>
                            <Card.Header>Results</Card.Header>
                            <Card.Body>
                                <Card.Title>Analysis: {id_analysis}</Card.Title>
                                <Card.Subtitle>Results List:</Card.Subtitle>
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