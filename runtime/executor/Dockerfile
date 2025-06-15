FROM python:3.13-slim-bookworm

WORKDIR /runtime
COPY ./ ./

RUN apt-get update && \
    apt-get install -y git bash tree && \
    rm -rf /var/lib/apt/lists/*

RUN pip install agitops

RUN python -m playwright install-deps && \
    python -m playwright install
