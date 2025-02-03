FROM alpine:3.10

LABEL maintainer="sajad.safarveisi@gmail.com"

RUN apk update && apk add --no-cache python py-pip py-setuptools git ca-certificates \
 && pip install --no-cache-dir python-dateutil python-magic \
 && git clone --depth=1 https://github.com/s3tools/s3cmd.git /opt/s3cmd \
 && rm -rf /opt/s3cmd/.git \
 && ln -s /opt/s3cmd/s3cmd /usr/bin/s3cmd \
 && apk del py-pip py-setuptools git

ADD ./entrypoint.sh /opt/entrypoint.sh

RUN chmod +x /opt/entrypoint.sh

WORKDIR /github/home
COPY ./.s3cfg ./.s3cfg

ENTRYPOINT ["/opt/entrypoint.sh"]