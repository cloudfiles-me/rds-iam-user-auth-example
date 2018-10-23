FROM python:3.6-alpine3.8 as base
FROM base as builder

LABEL Name  flask-app
LABEL version="1.0"
LABEL maintainer="jorgehrn at amazon"

USER root
RUN mkdir /install
WORKDIR /install
COPY requirements.txt .
RUN apk --no-cache add \
    --virtual build-dependencies \
    build-base \
    binutils \
    mariadb-client \
    mariadb-dev \
    mysql-client \
    libffi-dev \
    && pip install --no-cache-dir \
    --install-option="--prefix=/install" \
    -r requirements.txt \
    && apk del build-dependencies \
    && rm -rf /var/cache/apk/*

FROM base

COPY --from=builder /install /usr/local
ADD . /app
WORKDIR /app

EXPOSE 8080

CMD ["python3", "-m", "rds-iam-user-auth"]