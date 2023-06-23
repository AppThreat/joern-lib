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
ARG JAVA_VERSION=22.3.r19-grl

ENV JAVA_VERSION=$JAVA_VERSION \
    JAVA_HOME="/opt/java/${JAVA_VERSION}" \
    POLYNOTE_SCALA_VERSION=${SCALA_VERSION} \
    POLYNOTE_VERSION=${POLYNOTE_VERSION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING="utf-8"
ENV PATH=${PATH}:/root/.local/bin:${JAVA_HOME}/bin:
WORKDIR /opt

RUN set -e; \
    ARCH_NAME="$(rpm --eval '%{_arch}')"; \
    microdnf update -y && microdnf install -y gcc git-core python3.11 python3.11-devel python3.11-pip which wget tar zip \
        unzip sudo graphviz graphviz-gd graphviz-python3 findutils \
    && alternatives --install /usr/bin/python3 python /usr/bin/python3.11 1 \
    && python3 --version \
    && python3 -m pip install --upgrade pip \
    && curl -s "https://get.sdkman.io" | bash \
    && source "$HOME/.sdkman/bin/sdkman-init.sh" \
    && echo -e "sdkman_auto_answer=true\nsdkman_selfupdate_feature=false\nsdkman_auto_env=true" >> $HOME/.sdkman/etc/config \
    && sdk install java $JAVA_VERSION \
    && sdk offline enable \
    && mv /root/.sdkman/candidates/* /opt/ \
    && rm -rf /root/.sdkman \
    && curl -L https://github.com/AppThreat/cpggen/releases/latest/download/atomgen -o /usr/local/bin/atomgen \
    && chmod +x /usr/local/bin/atomgen \
    && atomgen --help \
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
    && chmod a-w -R /opt \
    && chown -R polly:polly /opt \
    && microdnf remove -y gcc findutils \
    && rm -rf /var/cache/yum \
    && microdnf clean all

EXPOSE 8192

ENTRYPOINT ["/opt/polynote/polynote.py"]
