# MultiCoCoA: Un Framework para Análisis Multimodal

## Description

It is a framework for multimodal analytics to facilitate data collection in collaborative activities. Efficiency and innovation in modern teams require conflict management skills and the creation of an inclusive environment, which are an integral part of workplace education and training. However, differences of opinion, lack of effective communication and other factors can generate interpersonal conflicts. To manage them, it is essential to develop and apply soft skills that can influence the formation of social, emotional and professional skills. MultiCoCoA, which uses machine learning techniques to analyze audio and video data, can help identify areas for improvement in communication and adjust behavior accordingly. The system is intuitive, allows data to be uploaded and analyzed, and presents the results in downloadable CSV files. The authors hope that MultiCoCoA will drive research in the field of communication and facilitate more effective practices in collaborative environments.

## Prerequisites

- To run this project you will need to have Docker installed on your system.

## Configuration

1. **Create a Docker network**: Run the following command to create a network called `mmla-network`.
    ```
    docker network create mmla-network
    ```
2. **Configuring Windows hosts**: Add `front.localhost` and `api.localhost` in your hosts file next to `localhost`..

## Deployment

### Deploy MongoDB and RabbitMQ databases:

```
docker-compose -f docker-compose.db.yml up -d
```

### Deploy Frontend and Backend:

```
docker-compose -f docker-compose.mmla.yml up -d
```

### Deploy system microservices:

To do this, you must move to the `engine` folder and execute the following commands:

```
docker-compose -f docker-compose.pa.yml up -d
docker-compose -f docker-compose.pv.yml up -d
```

### Deploy the output component of the system:

To do this, you must move to the `output` folder and execute the following command:

```
docker-compose up -d
```

Upon completion of these steps, you should have the entire system deployed and running.

## Uso

Once the system is deployed, you can access it from your web browser by entering the URL `front.localhost`.

## Contribution

We appreciate and value contributions to the project! If you want to contribute, follow the steps below:

- Make a fork of this repository and clone your copy on your local machine.
- Create a new branch for your contribution: git checkout -b name-of-your-branch.
- Make the necessary changes and perform meaningful commits.
- Make sure your code runs correctly and complies with the project's style guides.
- Submit a pull request describing your changes and explaining their purpose.
- Our team will review your request and provide comments or suggestions if necessary.
- Once your contribution is accepted, it will be merged with the main branch of the project.
We look forward to receiving your valuable contributions and appreciate your interest in improving this project!

## License

This project is distributed under the MIT License.

## Acknowledgments

This research was funded by grant ANID/FONDECYT/REGULAR/1211905.
