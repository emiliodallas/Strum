FROM python:3.10

WORKDIR /app

COPY . .

RUN python3 -m venv .venv && \
    . .venv/bin/activate && \
    apt-get update && \
    apt-get install -y iputils-ping && \
    touch .env && \
    echo "STEAM_API_KEY=6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE" >> .env && \
    pip3 install -r requirements.txt && \
    pip3 install -U steam[client]

EXPOSE 5000

CMD [ "python3", "./producer.py" ]
