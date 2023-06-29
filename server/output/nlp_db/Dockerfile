FROM python:3.9.12

WORKDIR /app

RUN apt-get update

COPY ./nlp_db/* ./
RUN pip3 install -r requirements.txt

COPY ./config/* ./
COPY ./helpers/* ./

ENTRYPOINT [ "python3" ]
CMD [ "nlp_db.py" ]