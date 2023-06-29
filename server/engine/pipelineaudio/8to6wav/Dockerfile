FROM python:3.9.12

WORKDIR /app

RUN apt-get update

COPY ./pipelineaudio/8to6wav/* ./
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "8to6wav.py" ]