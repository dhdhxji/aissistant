FROM mcr.microsoft.com/devcontainers/python:0-3.10

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt