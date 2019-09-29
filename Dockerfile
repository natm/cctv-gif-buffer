FROM alpine:3.10.2
MAINTAINER Nat Morris <nat@nuqe.net>

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools && \
    pip3 install virtualenv

ENV LIBRARY_PATH=/lib:/usr/lib
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

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

EXPOSE 8080/tcp

CMD ["/env/bin/python3", "/app/buffer.py", "-c /config/config.yaml"]
