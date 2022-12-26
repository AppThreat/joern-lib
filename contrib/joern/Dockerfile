FROM almalinux/9-minimal:latest

LABEL maintainer="ngcloudsec" \
      org.opencontainers.image.authors="Team ngcloudsec <cloud@ngcloud.io>" \
      org.opencontainers.image.source="https://github.com/ngcloudsec/joern-lib" \
      org.opencontainers.image.url="https://github.com/ngcloudsec/joern-lib" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="ngCloudSec" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="joern" \
      org.opencontainers.image.description="Container image for joern.io code analysis tool" \
      org.opencontainers.docker.cmd="docker run --rm -it -v /tmp:/tmp -p 7000:7000 -v $(pwd):/app:rw --cpus=2 --memory=8g -t ngcloudsec/joern joern -J-Xmx8g --server --server-host 0.0.0.0 --server-port 7000"

ENV JOERN_HOME /opt/joern/joern-cli
ENV PATH=${PATH}:/opt/joern/joern-cli:
RUN microdnf install -y git-core php php-cli python3 pcre2 which zip unzip sudo java-11-openjdk-headless \
    && curl -LO https://github.com/joernio/joern/releases/latest/download/joern-install.sh \
    && chmod +x ./joern-install.sh \
    && ./joern-install.sh \
    && useradd -ms /bin/bash joern \
    && chown -R joern:joern /opt/joern \
    && rm /joern-cli.zip /joern-install.sh \
    && rm -rf /var/cache/yum \
    && microdnf clean all
