FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

USER root

# Installing node
RUN apt-get update
RUN curl --silent --location https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs python-pytest

# Installing gulp
RUN npm install --global gulp-cli

WORKDIR /web
COPY ./package.json /web
RUN npm install

COPY ./app/requirements.txt /web/app/
# Install all the pip requirements
RUN mkdir /web/libs
RUN pip install -r /web/app/requirements.txt --target=/web/libs

COPY ./app /web/app

EXPOSE 8000

ENV PYTHONPATH $PYTHONPATH:/web:/web/libs
ENV FLASK_APP main:app

WORKDIR /web/app

