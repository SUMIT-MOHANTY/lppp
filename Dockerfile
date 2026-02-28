FROM ubuntu:22.04

LABEL maintainer="sandbox-team"
LABEL environment="sandbox"

ENV DEBIAN_FRONTEND=noninteractive
ENV APP_DIR=/app

RUN apt-get update && apt-get install -y     curl     git     docker.io     docker-compose     && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_DIR}

COPY . ${APP_DIR}

EXPOSE 80 443 22

CMD ["/bin/bash"]
