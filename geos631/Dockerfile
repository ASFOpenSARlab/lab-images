FROM ghcr.io/asfopensarlab/opensarlab:v1.1.1

USER root

RUN pip install igrf

# Lab specific setup
COPY geos631/hooks/geos631.sh /etc/user_server_includes/hooks/geos631.sh
COPY geos631/overrides/geos631.json /etc/user_server_includes/overrides/geos631.json

RUN chmod a+rx /etc/user_server_includes/hooks/geos631.sh

USER jovyan
