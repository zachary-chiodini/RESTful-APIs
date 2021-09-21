FROM ubuntu:20.04

LABEL maintainer="Zachary Chiodini"

# set env variables
ENV DEBIAN_FRONTEND noninteractive

# create working directory
WORKDIR /app

# copy contents to directory
COPY . .

# install packages
RUN apt update -y \
    && apt upgrade -y \
    && apt install python3.8 -y \
    && apt install python3-pip -y \
    && apt install default-libmysqlclient-dev -y \
    && /usr/bin/pip3 install -r requirements.txt \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# API port
EXPOSE 5000

CMD ["python3", "main.py"]
