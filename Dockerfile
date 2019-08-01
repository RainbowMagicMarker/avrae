FROM python:3.6-stretch

ARG DBOT_ARGS
ARG ENVIRONMENT=production

RUN useradd --create-home avrae
USER avrae
WORKDIR /home/avrae

COPY --chown=avrae:avrae requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

RUN mkdir temp

COPY --chown=avrae:avrae . .

COPY --chown=avrae:avrae docker/credentials-${ENVIRONMENT}.py credentials.py

# Download AWS pubkey to connect to documentDB
RUN if [ "$ENVIRONMENT" = "production" ]; then wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem; fi

ENTRYPOINT .local/bin/newrelic-admin run-program python dbot.py $DBOT_ARGS