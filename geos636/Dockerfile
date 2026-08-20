FROM ghcr.io/asfopensarlab/deployment-opensarlab-container_sar:v1.3.2

USER root

# Lab specific setup
COPY geos636/hooks/geos636.sh /etc/user_server_includes/hooks/geos636.sh
COPY geos636/overrides/geos636.json /etc/user_server_includes/overrides/geos636.json

RUN chmod a+rx /etc/user_server_includes/hooks/geos636.sh

USER jovyan

# Run Locally:
# docker \
#     run \
#     -it \
#     -p 8888:8888 \
#     -u root \
#     -v $PWD/geos636/hooks/geos636.sh:/usr/local/bin/before-notebook.d/start.sh
#     geos636