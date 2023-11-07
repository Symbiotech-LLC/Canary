    FROM python:3.11.6-alpine3.18

    ARG WEB_PORT=8080
    ARG APP_USER=canary
    ARG USER_UID=1000
    ARG USER_GID=$USER_UID
    ENV WEB_PORT=${WEB_PORT}
    ENV HOME /home/Canary

    EXPOSE ${WEB_PORT}/TCP

    WORKDIR ${HOME}

    COPY ./src ${HOME}/src
    COPY ./canary.py ${HOME}/canary.py
    COPY ./requirements.txt ${HOME}/requirements.txt

    RUN apk add shadow

    # Create a group and user
    RUN addgroup --system --gid ${USER_GID} ${APP_USER}
    RUN adduser --system --disabled-password --home ${HOME} --uid ${USER_UID} --ingroup ${APP_USER} ${APP_USER}
    USER $APP_USER

    RUN python -m pip install --upgrade pip
    RUN python -m pip install -r requirements.txt

    ENTRYPOINT ["tail", "-f", "/dev/null"]

    # # Start running the server
    # # ENTRYPOINT node $FOUNDRY_APP/resources/app/main.js --dataPath=$FOUNDRY_DATA  && tail -f /dev/null
    # CMD sh $HOME/scripts/start_foundry.sh && tail -f /dev/null