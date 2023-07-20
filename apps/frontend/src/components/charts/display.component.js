import React, { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import chartService from '../../services/chart.service';
import Spinner from "react-bootstrap/Spinner";

const Display = (props) => {
    const [spinner, setSpinner] = useState(true);
    const [imageData, setImageData] = useState(null);
    const chart = props.obj;

    useEffect(() => {
        const fetchImage = async () => {
            chartService.get(chart.url).then((response) => {
                console.log(response)
                let base64 = btoa(
                    new Uint8Array(response.data).reduce(
                        (data, byte) => data + String.fromCharCode(byte),
                        '',
                    ),
                );
                setImageData(`data:${response.headers['content-type'].toLowerCase()};base64,${base64}`);
                setSpinner(false);
            }).catch((error) => {
                console.log(error);
                setSpinner(false);
            });
        };
        fetchImage();
    }, []);

    return (
        <Row className="p-2">
            <Col>
                {spinner ? (
                    <Spinner animation="border" role="status" variant="primary">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
                ) : (
                    <Image src={imageData} alt="Imagen cargada desde el API REST 1" fluid/>
                )}
            </Col>
        </Row>

    );
};

export default Display;
