FROM node:22-alpine

WORKDIR /server

COPY . .

RUN npm install
RUN mkdir -p files

EXPOSE 3000

CMD ["npm", "start"]
