FROM python:3.13-alpine

WORKDIR /runtime
COPY ./ ./

RUN apk update && apk add git bash tree
RUN pip install agitops
RUN python -m playwright install-deps && python -m playwright install
