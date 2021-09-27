FROM ubuntu:20.04

LABEL maintainer="Zachary Chiodini" \
      name="chem-trans-api" \
      version="1.0"

# set env variables
ENV DEBIAN_FRONTEND noninteractive

# create working directory
WORKDIR /app

# copy contents to directory
COPY . .

# install packages
RUN apt update -y
RUN apt upgrade -y
RUN apt install python3.8 -y
RUN apt install python3-pip -y
RUN apt install default-libmysqlclient-dev -y
RUN /usr/bin/pip3 install -r requirements.txt -y
RUN apt-get clean autoclean
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/*

# API port
EXPOSE 5000

CMD ["python3", "main.py"]
