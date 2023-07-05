FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y iputils-ping
RUN pip3 install -r requirements.txt

CMD [ "python", "./consumer.py" ]