# docker image base
FROM python:3.10

# setup environment variable
ENV HOME_DOCKER=/home/app/webapp

# set work directory
RUN mkdir -p $HOME_DOCKER

# where your code lives
WORKDIR $HOME_DOCKER

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $HOME_DOCKER

# install requirements
RUN pip install -r requirements.txt

# port django
EXPOSE 8000

# start server
CMD python manage.py runserver