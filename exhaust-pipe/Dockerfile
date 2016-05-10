# Starting from Python 2.7 alpine image
FROM python:2.7-alpine
MAINTAINER Gert Leenders <leenders.gert@gmail.com>

# Add a user to allow this container to run as non-root
RUN addgroup -g 1001 exhaust && adduser -D -G exhaust -s /bin/false -u 1001 exhaust

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY resources ./resources
COPY exhaust-pipe.py ./

RUN chown -R exhaust:exhaust ./

USER exhaust

CMD python exhaus-pipe.py
