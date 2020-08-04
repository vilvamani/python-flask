# pull official base image
FROM python:3.8.1-slim-buster

# set maintainer
LABEL maintainer "vilvamani007@gmail.com"

ARG build_no=not_set
ARG git_commit_id=not_set

LABEL BUILD_NO=$build_no
LABEL GIT_COMMIT_ID=$git_commit_id

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# copy project
COPY . /usr/src/app/
CMD python /usr/src/app/flaskr/app.py run -h 0.0.0.0