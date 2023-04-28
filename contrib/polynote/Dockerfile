FROM almalinux/9-minimal:latest

LABEL maintainer="appthreat" \
      org.opencontainers.image.authors="Team AppThreat <cloud@appthreat.com>" \
      org.opencontainers.image.source="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.url="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.version="0.6.5" \
      org.opencontainers.image.vendor="AppThreat" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="polynote" \
      org.opencontainers.image.description="Container image for polynote" \
      org.opencontainers.docker.cmd="docker run --rm -it -v /tmp:/tmp -p 8192:8192 -v $(pwd):/opt/notebooks:rw --cpus=2 --memory=4g -t ghcr.io/appthreat/polynote"

ARG POLYNOTE_VERSION="0.5.0"
ARG SCALA_VERSION="2.12"
ARG DIST_TAR="polynote-dist.tar.gz"
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
WORKDIR /opt

RUN microdnf install -y gcc git-core python3 python3-devel which wget tar zip unzip sudo java-17-openjdk-devel \
    && wget -q https://github.com/polynote/polynote/releases/download/$POLYNOTE_VERSION/$DIST_TAR \
    && tar xfzp $DIST_TAR \
    && echo "DIST_TAR=$DIST_TAR" \
    && rm $DIST_TAR \
    && pip install -r ./polynote/requirements.txt \
    && pip install poetry GitPython pandas matplotlib \
    && useradd -ms /bin/bash polly \
    && chown -R polly:polly /opt \
    && microdnf remove -y gcc \
    && rm -rf /var/cache/yum \
    && microdnf clean all

USER polly
EXPOSE 8192
ENV POLYNOTE_SCALA_VERSION=${SCALA_VERSION} \
    POLYNOTE_VERSION=${POLYNOTE_VERSION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING="utf-8"

ENTRYPOINT ["/opt/polynote/polynote.py"]
