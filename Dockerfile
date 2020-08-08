# pull official base image
FROM python:3.8.1-slim-buster

# set maintainer
LABEL maintainer "vilvamani007@gmail.com"

# set work directory
WORKDIR /

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# copy project
COPY . /
CMD python /app/run.py run -h 0.0.0.0