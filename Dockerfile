FROM ubuntu:20.04

WORKDIR /app

COPY . /app/

RUN apt-get update

# Install python
RUN echo "Y" | apt install python3.8

# Install pip
RUN echo "Y" | apt install python3-pip

# Install library for mysqlclient
RUN echo "Y" | apt install default-libmysqlclient-dev

# Install backend dependencies
RUN /usr/bin/pip3 install -r /app/flask-api/requirements.txt

# Expose port
EXPOSE 5011
