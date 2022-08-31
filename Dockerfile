# pull official base image
FROM python:3.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

CMD [ "python", "src/app.py" ]