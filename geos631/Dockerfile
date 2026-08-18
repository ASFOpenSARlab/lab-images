FROM ghcr.io/asfopensarlab/deployment-opensarlab-container_sar:v1.3.2

USER root

# Lab specific setup
COPY geos631/hooks/geos631.sh /etc/user_server_includes/hooks/geos631.sh
COPY geos631/overrides/geos631.json /etc/user_server_includes/overrides/geos631.json

RUN chmod a+rx /etc/user_server_includes/hooks/geos631.sh

USER jovyan

# Run Locally:
# docker \
#     run \
#     -it \
#     -p 8888:8888 \
#     -u root \
#     -v $PWD/geos631/hooks/geos631.sh:/usr/local/bin/before-notebook.d/start.sh
#     geos631