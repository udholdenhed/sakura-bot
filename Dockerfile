FROM python:3-alpine

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install python-telegram-bot -U --pre

CMD [ "python", "./main.py"]