# syntax=docker/dockerfile:1
FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip
