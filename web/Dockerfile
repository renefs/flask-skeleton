FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

# Installing node
RUN apt-get update
RUN curl --silent --location https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs

# Installing gulp
RUN npm install --global gulp-cli

WORKDIR /web
COPY ./package.json /web
RUN npm install

COPY ./app/requirements.txt /web/app/
# Install all the pip requirements
RUN pip install -r /web/app/requirements.txt

COPY ./app /web/app

ENV PYTHONPATH $PYTHONPATH:/web

