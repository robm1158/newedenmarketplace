# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /code
COPY .\requirements /code

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    awscli