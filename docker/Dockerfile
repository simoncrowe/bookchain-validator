FROM python:3.7

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libssl-dev \
        supervisor && \
        mkdir /run/nginx  && \
        mkdir /var/log/gunicorn
COPY ./src /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    python -m spacy download en_core_web_sm  && \
    pip install gunicorn


COPY ./docker/supervisord.conf /etc/supervisord/supervisord.conf

WORKDIR /app

ENV PYTHONPATH=/app

EXPOSE 8008

ENTRYPOINT ["supervisord", "-c", "/etc/supervisord/supervisord.conf"]
