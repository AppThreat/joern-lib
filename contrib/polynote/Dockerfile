FROM almalinux:9.2-minimal

LABEL maintainer="appthreat" \
      org.opencontainers.image.authors="Team AppThreat <cloud@appthreat.com>" \
      org.opencontainers.image.source="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.url="https://github.com/appthreat/joern-lib" \
      org.opencontainers.image.version="0.11.1" \
      org.opencontainers.image.vendor="AppThreat" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="polynote" \
      org.opencontainers.image.description="Container image for code and threat analysis with polynote" \
      org.opencontainers.docker.cmd="docker run --rm -it -v /tmp:/tmp -p 8192:8192 -v $(pwd):/opt/notebooks:rw -t ghcr.io/appthreat/polynote"

ARG POLYNOTE_VERSION="0.5.1"
ARG SCALA_VERSION="2.12"
ARG DIST_TAR="polynote-dist.tar.gz"
ARG TARGETPLATFORM

ENV ATOM_VERSION=1.0.0 \
    ATOM_HOME=/opt/atom-1.0.0 \
    JAVA_HOME="/opt/graalvm-ce-java19-22.3.1" \
    PATH=${PATH}:/root/.local/bin:/opt/atom-1.0.0/bin:
WORKDIR /opt

RUN set -e; \
    ARCH_NAME="$(rpm --eval '%{_arch}')"; \
    microdnf update -y && microdnf install -y gcc git-core python3.11 python3.11-devel python3.11-pip which wget tar zip \
        unzip sudo graphviz graphviz-gd graphviz-python3 \
    && alternatives --install /usr/bin/python3 python /usr/bin/python3.11 1 \
    && python3 --version \
    && python3 -m pip install --upgrade pip \
    && bash <(curl -sL https://get.graalvm.org/jdk) --to /opt graalvm-ce-java19-22.3.1 \
    && curl -LO https://github.com/AppThreat/atom/releases/latest/download/atom.zip \
    && curl -LO https://github.com/AppThreat/atom/releases/latest/download/atom.zip.sha512 \
    && echo "$(cat atom.zip.sha512 | cut -d ' ' -f1) atom.zip" | sha512sum -c \
    && unzip -q atom.zip -d /opt/ \
    && rm atom.zip \
    && ln -s /opt/atom-${ATOM_VERSION}/bin/atom /usr/local/bin/atom \
    && curl -LO https://repo.almalinux.org/almalinux/9/CRB/${ARCH_NAME}/os/Packages/graphviz-devel-2.44.0-25.el9.${ARCH_NAME}.rpm \
    && rpm -ivh graphviz-devel-2.44.0-25.el9.${ARCH_NAME}.rpm \
    && rm graphviz-devel-2.44.0-25.el9.${ARCH_NAME}.rpm \
    && pip install virtualenv ipython nbconvert numpy jedi jep GitPython pandas matplotlib graphviz pydotplus networkx[default,extra] \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install torch_geometric pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cpu.html \
    && wget -q https://github.com/polynote/polynote/releases/download/$POLYNOTE_VERSION/$DIST_TAR \
    && tar xfzp $DIST_TAR \
    && echo "DIST_TAR=$DIST_TAR" \
    && rm $DIST_TAR \
    && useradd -ms /bin/bash polly \
    && chown -R polly:polly /opt \
    && microdnf remove -y gcc \
    && rm -rf /var/cache/yum \
    && microdnf clean all

EXPOSE 8192
ENV POLYNOTE_SCALA_VERSION=${SCALA_VERSION} \
    POLYNOTE_VERSION=${POLYNOTE_VERSION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING="utf-8"

ENTRYPOINT ["/opt/polynote/polynote.py"]
