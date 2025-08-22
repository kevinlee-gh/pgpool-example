FROM ubuntu:20.04

RUN apt update && apt install -y software-properties-common && add-apt-repository -y --update ppa:ansible/ansible && apt install -y ansible iputils-ping telnet curl
RUN ansible-galaxy collection install community.docker
ENV ANSIBLE_HOST_KEY_CHECKING=False
WORKDIR /workspace