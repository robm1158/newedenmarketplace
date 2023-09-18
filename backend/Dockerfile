# syntax=docker/dockerfile:1
FROM python3:latest AS development

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip
RUN apt-get install -y build-essential