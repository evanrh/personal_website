FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD . /app
ADD docker/config/wsgi/boot.sh ./
RUN chmod +x boot.sh

RUN pip3 install -r requirements.txt
ENTRYPOINT ["./boot.sh"]
