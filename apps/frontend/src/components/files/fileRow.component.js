import React, { useState } from "react";
import { Button } from "react-bootstrap";
//import { useNavigate  } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ModalAnalyzeActivity from "../analysis/modalAnalyzeActivity";

const FileRow = (props) => {
    const { filename, type, length } = props.obj;
    //let navigate = useNavigate();   
    const [modalShow, setModalShow] = useState(false);

    const play = () => {
        //play file
    };

    const download = () => {
        //download file
    };

    const remove = () => {
        //remove
    };

    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{filename}</div>
            </div>
            <div className="ms-2 me-auto">
                {type}
            </div>
            <div className="ms-2 me-auto">
                {length}
            </div>
            <ButtonGroup aria-label="actions">
                <Button onClick={(play)} variant="outline-primary">
                    <i className="bi bi-play"></i>
                </Button>
                <Button onClick={() => setModalShow(true)} variant="outline-primary">
                    <i className="bi bi-search"></i>
                </Button>
                <Button onClick={download} variant="outline-secondary">
                    <i className="bi bi-cloud-arrow-down"></i>
                </Button>
                <Button onClick={remove} variant="outline-danger">
                    <i className="bi bi-trash"></i>
                </Button>
            </ButtonGroup>
            <ModalAnalyzeActivity
                show={modalShow}
                onHide={() => setModalShow(false)}
                file={filename}
            />
        </ListGroup.Item>
    );
}

export default FileRow;