FROM python:3.7.2-slim

# set working directory
WORKDIR /usr/src/app
COPY . /usr/src/app

# install requirements
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1