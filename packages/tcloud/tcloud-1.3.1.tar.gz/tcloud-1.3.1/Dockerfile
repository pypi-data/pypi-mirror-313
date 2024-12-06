FROM python:3.12-slim

ARG TCLOUD_VERSION=""

RUN pip3 install "tcloud==${TCLOUD_VERSION}"

ENTRYPOINT ["tcloud"]
