#!/usr/bin/env bash

NAME="web-exposed"

cd private
docker build -t ${NAME} -f Containerfile .

docker rm -f ${NAME}
docker run -d \
    --restart=always \
    --name=${NAME} \
    -p 80:80 \
    ${NAME}
