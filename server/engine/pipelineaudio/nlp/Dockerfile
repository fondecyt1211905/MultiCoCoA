FROM python:3.9.12

WORKDIR /app

RUN apt-get update

COPY ./pipelineaudio/nlp/* ./
RUN pip3 install --trusted-host=github.com --default-timeout=180 -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "nlp.py" ]