# Starting from Python 3.5 alpine image
FROM python:3.5-alpine
MAINTAINER Gert Leenders <leenders.gert@gmail.com>

# Add a user to allow this container to run as non-root
RUN addgroup -g 1001 exhaust && adduser -D -G exhaust -s /bin/false -u 1001 exhaust

RUN mkdir /data
RUN chown -R exhaust:exhaust /data
VOLUME ["/data"]

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY resources ./resources
COPY *.py ./

RUN chown -R exhaust:exhaust ./

USER exhaust

CMD python exhaust-pipe.py
