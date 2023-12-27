FROM python:3.8-slim
ENV BOT_NAME="kartpaybot"

WORKDIR /app
RUN mkdir app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
