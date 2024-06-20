FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y postgresql libpq-dev postgresql-client gcc && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -r -s /bin/bash manuel

ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R manuel:manuel /app
USER manuel

ENV FLASK_ENV=production

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG POSTGRES_USER
ARG POSTGRES_PW
ARG POSTGRES_HOST
ARG POSTGRES_DB
ARG JWT_SECRET_KEY

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PW=$POSTGRES_PW
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_DB=$POSTGRES_DB
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]