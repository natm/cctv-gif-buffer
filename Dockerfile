FROM phusion/baseimage:0.9.18
MAINTAINER Nat Morris <nat@nuqe.net>

RUN apt-get update -y

RUN apt-get -y autoremove

EXPOSE 8888/tcp
