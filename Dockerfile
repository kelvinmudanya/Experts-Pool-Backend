# base image
FROM python:3.8.2

# maintainer
MAINTAINER SamFast

# copy the application folder into the docker file
ADD . /usr/src/app

## set the default working directory
WORKDIR /usr/src/app

COPY requirements.txt ./

# install requirements using pip
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN ls -a
## expose ports
EXPOSE 80

## default command to execute

CMD exec gunicorn bimaapi.wsgi:application --bind 0.0.0.0:80 --workers 3
