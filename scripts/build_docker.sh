#!/bin/bash

source ./.env

echo "APP Version: ${APP_VERSION}"
echo "Web Port: ${WEB_PORT}"


function build_docker() {
    docker build -t canary:${APP_VERSION} \
    --build-arg "APP_USERNAME=${APP_USERNAME}" \
    --build-arg "WEB_PORT=${WEB_PORT}" \
    ../

}


build_docker