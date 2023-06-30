FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y iputils-ping
RUN touch .env
RUN echo  "STEAM_API_KEY=6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE" >> .env
RUN pip3 install -r requirements.txt
RUN pip3 install -U steam[client]

EXPOSE 5000

CMD [ "python", "./producer.py" ]