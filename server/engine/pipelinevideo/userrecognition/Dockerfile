FROM python:3.9.12

WORKDIR /root/.deepface/weights
WORKDIR /app

RUN apt-get update
RUN apt install -y libgl1

COPY ./pipelinevideo/userrecognition/* ./
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "userrecognition.py" ]
