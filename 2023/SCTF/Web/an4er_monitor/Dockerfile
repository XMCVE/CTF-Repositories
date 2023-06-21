FROM ubuntu:latest

RUN apt-get update

#server
RUN apt-get install -y nodejs npm redis-server 

COPY redis.conf /etc/redis/redis.conf
RUN mkdir /run/redis/

RUN apt-get install -y nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80


RUN mkdir /app
COPY src/server /app/server
WORKDIR /app/server

RUN npm install


WORKDIR /app
COPY src/build.sh /app
RUN chmod 777 build.sh

RUN rm -rf /usr/share/nginx/html
COPY src/front/dist/ /usr/share/nginx/html

ENTRYPOINT ["bash","build.sh"]

