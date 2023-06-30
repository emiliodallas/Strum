FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y iputils-ping
RUN pip3 install -r requirements.txt

EXPOSE 5000


CMD [ "python", "./consumer.py" ]