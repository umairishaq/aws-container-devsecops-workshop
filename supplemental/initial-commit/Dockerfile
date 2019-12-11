FROM python:3.7-alpine

LABEL maintainer="Sasquatch"

RUN apk add --no-cache sqlite-libs=3.28.0-r1 git=2.22.0-r0

COPY . /app

WORKDIR /app

RUN git clone https://github.com/todb-r7/eicar.git

RUN pip install -r requirements.txt

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

EXPOSE 5000

USER root

CMD python ./index.py