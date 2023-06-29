import React, { useState, useEffect } from "react";
//import { useNavigate  } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import AnalysisService from "../../services/analysis.service";
import AnalysisRow from "./analysisRow.component";


export default function Analysis(){
    const [analysis, setAnalysis] = useState([]);
    //let navigate = useNavigate(); 
  
    useEffect(() => {
        AnalysisService.getAll().then(({ data }) => {
            setAnalysis(data);
        }).catch((error) => {
            console.log(error);
        });
    }, []);


    const DataElements = () => {
        return analysis.map((res, i) => {
            //console.log(res)
            return <AnalysisRow obj={res} key={i} />;
        });
    };
    return (
        <>
            <Container fluid="md text-start">
                <Row className="p-2">
                    <Col>
                        <Card>
                            <Card.Header>Analysis</Card.Header>
                            <Card.Body>
                                <Card.Title>Analysis list:</Card.Title>
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
