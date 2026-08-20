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
#     --entrypoint bash \
#     ghcr.io/asfopensarlab/geos636 \
#         -c " \
#               /etc/user_server_includes/hooks/geos636.sh &&  \
#               tini -g -- start.sh start-notebook.py \
#            "