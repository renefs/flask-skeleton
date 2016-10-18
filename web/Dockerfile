FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

# Installing node
RUN apt-get update
RUN apt-get install sudo
RUN curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash - && sudo apt-get install -y nodejs
RUN node -v

# Installing gulp
RUN npm install --global gulp-cli
RUN gulp -v

COPY . /web

# Install all the pip requirements
RUN pip install -r /web/app/requirements.txt


WORKDIR /web
RUN npm install

WORKDIR /web/app

