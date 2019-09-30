FROM ubuntu:18.04
MAINTAINER Nat Morris <nat@nuqe.net>

RUN apt-get update && apt-get install -y \
    python3 \
    build-essential \
    python3-setuptools \
    python-dev \
    python3-pip

RUN pip3 install virtualenv

# Copy requirements before app so we can cache PIP dependencies on their own
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN virtualenv -p python3 /env && /env/bin/pip3 install -r /app/requirements.txt

COPY buffer.py /app/
COPY cctvgifbuffer/*.py /app/cctvgifbuffer/

RUN rm -rf \
	         /root/.cache \
	        /tmp/*
RUN rm -rf /var/cache/apk/*

RUN apt-get autoremove -y; \
     apt-get autoclean -y

EXPOSE 8001/tcp

CMD ["/env/bin/python3", "/app/buffer.py", "-c /config/config.yaml"]
