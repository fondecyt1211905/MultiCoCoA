import React, { useState, useEffect} from "react";
import { useParams} from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import IndicatorRow from "./indicatorRow.component";
import analysisService from "../../services/analysis.service";
import Display from "../charts/display.component";

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


    const chartElements = () => {
        const url = [
            {"url": "/chart/chart1/" + id_analysis},
            {"url": "/chart/chart2/" + id_analysis},
            {"url": "/chart/chart3/" + id_analysis},
            {"url": "/chart/chart4/" + id_analysis},
            {"url": "/chart/chart5/" + id_analysis}
        ];
        return url.map((res, i) => {
            return <Display obj={res} key={i}/>;
        });
    };

    const DownloadElements = () => {
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
                            <Card.Header>Results download </Card.Header>
                            <Card.Body>
                                <Card.Subtitle>List of indicators:</Card.Subtitle>
                                <ListGroup as="ol" numbered>
                                    {DownloadElements()}
                                </ListGroup>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
            <Container fluid="md text-start">
                <Row className="p-2">
                    <Col>
                        <Card>
                            <Card.Header>Results graphs</Card.Header>
                            <Card.Body>
                                <Container>
                                        {chartElements()}
                                </Container>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    );
}