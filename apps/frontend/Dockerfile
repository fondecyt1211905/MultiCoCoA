FROM node:13.12.0-alpine

WORKDIR /usr/src/frontend

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend ./

EXPOSE 80

CMD ["npm", "start"]
