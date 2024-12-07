FROM  almalinux:9.2

LABEL maintainer="Natthan Pigoux <natthan.pigoux@lupm.in2p3.fr>, Luisa Arrabito <arrabito@in2p3.fr>"
LABEL description="CTADIRAC client docker image"
LABEL org.opencontainers.image.url=https://gitlab.cta-observatory.org/cta-computing/dpps/CTADIRAC

ENV DIRAC_DIR="/home/dirac"

RUN groupadd -r dirac \
    && useradd --no-log-init -r -g dirac dirac

RUN mkdir -p ${DIRAC_DIR} \
    && mkdir -p /CTADIRAC

COPY ./ /CTADIRAC/

COPY ${CI_PROJECT_DIR}/docker/dirac-client/EGI-trustanchors.repo ${DIRAC_DIR}

RUN cat ${DIRAC_DIR}/EGI-trustanchors.repo > /etc/yum.repos.d/EGI-trustanchors.repo

RUN yum install -y ca-policy-egi-core && yum clean all

#-> need to specify pkg version
# hadolint ignore=DL3041
RUN dnf update -y && \
    dnf install -y  git wget make && \
    dnf clean all

WORKDIR ${DIRAC_DIR}
RUN git clone https://github.com/ubuntu-cern/fetch-crl.git
WORKDIR ${DIRAC_DIR}/fetch-crl
RUN make install

WORKDIR ${DIRAC_DIR}
RUN rm -f ${DIRAC_DIR}/EGI-trustanchors.repo
COPY --chmod=774 ${CI_PROJECT_DIR}/docker/dirac-client/Entrypoint.sh /home/dirac/

RUN chown -R dirac:dirac ${DIRAC_DIR} && \
    chown -R dirac:dirac /CTADIRAC

ENTRYPOINT [ "/home/dirac/Entrypoint.sh" ]
CMD ["/bin/bash"]

# Install DIRAC client
USER dirac
# hadolint ignore=SC1091,SC2086
RUN curl -LO https://github.com/DIRACGrid/DIRACOS2/releases/latest/download/DIRACOS-Linux-x86_64.sh \
    && bash DIRACOS-Linux-x86_64.sh -p ${DIRAC_DIR}/diracos \
    && rm -f DIRACOS-Linux-x86_64.sh \
    && ln -s /etc/grid-security/certificates/ ${DIRAC_DIR}/diracos/etc/grid-security/certificates \
    && source ${DIRAC_DIR}/diracos/diracosrc; pip install --no-cache-dir /CTADIRAC/

USER root
RUN rm -rf /CTADIRAC

USER dirac
