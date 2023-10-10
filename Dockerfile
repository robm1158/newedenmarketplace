# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /code

# Install system dependencies and add Node.js from Nodesource
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    build-essential \
    libssl-dev \
    && curl -sL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# You can verify the installed version of Node.js
RUN node -v
RUN npm -v

# Upgrade pip (if needed)
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /code
RUN pip install -r requirements.txt
