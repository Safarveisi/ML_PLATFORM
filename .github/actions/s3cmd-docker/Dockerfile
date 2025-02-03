FROM alpine:3.10

LABEL maintainer="sajad.safarveisi@gmail.com"

RUN apk update && apk add --no-cache python py-pip py-setuptools git ca-certificates \
    && pip install --no-cache-dir python-dateutil python-magic \
    && git clone --depth=1 --branch v2.4.0 https://github.com/s3tools/s3cmd.git /tmp/s3cmd \
    && rm -rf /tmp/s3cmd/.git \
    && cd /tmp/s3cmd && python setup.py install \
    && apk del py-pip py-setuptools git \
    && rm -rf /tmp/s3cmd

COPY ./entrypoint.sh /opt/s3cmd/entrypoint.sh
RUN chmod u+x /opt/s3cmd/entrypoint.sh

WORKDIR /github/home
COPY ./.s3cfg .s3cfg

ENTRYPOINT ["/opt/s3cmd/entrypoint.sh"]