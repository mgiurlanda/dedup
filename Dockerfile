FROM python:3.7-alpine

RUN apk add --no-cache --update python3-dev  gcc build-base
RUN adduser -D dedup

WORKDIR /home/dedup

RUN apk --update add --no-cache g++

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY dedup.py boot.sh ./

RUN dos2unix dedup.py dedup.py
RUN dos2unix boot.sh boot.sh

RUN chmod +x boot.sh

ENV FLASK_APP dedup.py

RUN chown -R dedup:dedup ./
USER dedup

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]