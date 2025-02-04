FROM alpine:3.10

LABEL maintainer="sajad.safarveisi@gmail.com"

RUN apk update && apk add --no-cache python py-pip py-setuptools git ca-certificates \
    && pip install --no-cache-dir s3cmd==2.4.0

ADD ./entrypoint.sh /opt/s3cmd/entrypoint.sh
ADD ./.s3cfg .s3cfg

RUN chmod u+x /opt/s3cmd/entrypoint.sh

WORKDIR /github/home

ENTRYPOINT ["/opt/s3cmd/entrypoint.sh"]