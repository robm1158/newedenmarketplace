# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /code
COPY requirements.txt /code

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    awscli
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs
# RUN npm install
