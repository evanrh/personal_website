FROM python:3.8-slim
RUN mkdir /app
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev \
	gcc libpq-dev
WORKDIR /app
ADD requirements.txt /app
ADD . /app
ADD docker/config/wsgi/boot.sh ./
RUN chmod +x boot.sh

RUN pip3 install -r requirements.txt
ENTRYPOINT ["./boot.sh"]
