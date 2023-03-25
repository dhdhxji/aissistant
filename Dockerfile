FROM mcr.microsoft.com/devcontainers/python:0-3.10

RUN apt-get update
RUN apt-get install -y portaudio19-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt