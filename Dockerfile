FROM registry.access.redhat.com/rhscl/python-36-rhel7

#ENV ARTIFACT_URL

USER root

ADD files /

RUN yum repolist all

#RUN yum -y update && \
#    yum install -y wget && \
#    chmod u+x /install_dumb_init.sh && \
#    /install_dumb_init.sh
RUN pip install --upgrade pip && \
    pip install ansible-tower-cli && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]