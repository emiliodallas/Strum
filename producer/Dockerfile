FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install

RUN touch .env && \
    echo "STEAM_API_KEY=6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE" >> .env

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "./producer.py" ]
