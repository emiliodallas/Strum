FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "./sql.py" ]
