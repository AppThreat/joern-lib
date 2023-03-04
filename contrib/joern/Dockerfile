FROM almalinux/9-minimal:latest

LABEL maintainer="appthreat" \
      org.opencontainers.image.authors="Team AppThreat <cloud@appthreat.com>" \
      org.opencontainers.image.source="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.url="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.version="0.6.3" \
      org.opencontainers.image.vendor="AppThreat" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="joern" \
      org.opencontainers.image.description="Container image for joern.io code analysis tool" \
      org.opencontainers.docker.cmd="docker run --rm -it -v /tmp:/tmp -p 9000:9000 -v $(pwd):/app:rw --cpus=2 --memory=8g -t ghcr.io/appthreat/joern joern -J-Xmx8g --server --server-host 0.0.0.0 --server-port 9000"

ENV JOERN_HOME=/opt/joern/joern-cli \
    PATH=${PATH}:/opt/joern/joern-cli:
RUN microdnf install -y git-core php php-cli python3 pcre2 which zip unzip sudo java-17-openjdk-headless ncurses \
    && curl -LO https://github.com/joernio/joern/releases/latest/download/joern-install.sh \
    && chmod +x ./joern-install.sh \
    && ./joern-install.sh \
    && mkdir -p /opt/joern/custom_scripts \
    && useradd -ms /bin/bash joern \
    && chown -R joern:joern /opt/joern \
    && rm /joern-cli.zip /joern-install.sh \
    && rm -rf /var/cache/yum \
    && microdnf clean all
