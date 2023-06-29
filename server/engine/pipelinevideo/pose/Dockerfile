FROM python:3.9.12

WORKDIR /app

RUN apt-get update
RUN apt install -y libgl1

COPY ./pose/requirements.txt requirements.txt
COPY ./pose/pose.py pose.py
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "pose.py" ]