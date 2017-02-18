FROM phusion/baseimage:0.9.19
MAINTAINER Nat Morris <nat@nuqe.net>


RUN apt-get update && apt-get install -y python-pip && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove curl

RUN pip install virtualenv

COPY . /app
WORKDIR /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8080/tcp
