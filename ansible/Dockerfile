FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y software-properties-common iputils-ping telnet curl python3-pip

RUN add-apt-repository -y --update ppa:ansible/ansible && apt install -y ansible

RUN ansible-galaxy collection install community.docker community.postgresql
RUN pip3 install psycopg2-binary

WORKDIR /workspace