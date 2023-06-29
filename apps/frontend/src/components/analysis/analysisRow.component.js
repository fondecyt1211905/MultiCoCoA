import React from "react";
import { Button } from "react-bootstrap";
import { useNavigate  } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import analysisService from "../../services/analysis.service";

const AnalysisRow = (props) => {
    const { id, time, name, start, end } = props.obj;
    let navigate = useNavigate();  

    const GotoIndicator = () => {
        navigate("/Indicator/" + id);
    };

    const removeAnalysis = () => {
        analysisService.remove(id)
            .then(response => {
                window.location.reload();
            }).catch(err => {
                console.log(err)
            })
    };
    
    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{name}</div>
                {id}
            </div>
            <div className="ms-2 me-auto">
                {time}
            </div>
            <div className="ms-2 me-auto">
                {start}-{end}
            </div>
            <ButtonGroup aria-label="actions">
                <Button onClick={GotoIndicator} variant="outline-primary">
                    <i className="bi bi-bar-chart-line"> Indicators</i>
                </Button>
                <Button onClick={removeAnalysis} variant="outline-danger">
                    <i className="bi bi-trash"> Remove</i>
                </Button>
            </ButtonGroup>
        </ListGroup.Item>
    );
  };
    
  export default AnalysisRow;