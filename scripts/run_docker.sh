#!/bin/bash

source ./.env

echo "APP Version: ${APP_VERSION}"
echo "Web Port: ${WEB_PORT}"


function run_docker() {
    docker run -t \
    --rm \
    --name=canary \
    --env-file ./.env \
    -p ${WEB_PORT}:${WEB_PORT} \
    -it --entrypoint sh \
    -v $(pwd)/Results:/home/$APP_USERNAME/Results \
    canary:${APP_VERSION}

    # --mount type=bind,src=$DATA_MOUNT,dst=$FOUNDRY_DIR/data \
}


run_docker