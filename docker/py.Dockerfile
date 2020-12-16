FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD . /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["gunicorn", "resume:create_app()", "-b", "0.0.0.0:8000"]
