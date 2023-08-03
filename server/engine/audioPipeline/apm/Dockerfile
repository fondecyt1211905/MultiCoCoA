FROM python:3.9.12

WORKDIR /app

RUN apt-get update
RUN apt-get install libasound-dev libsndfile1-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y

COPY ./audioPipeline/apm/* ./
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "apm.py" ]