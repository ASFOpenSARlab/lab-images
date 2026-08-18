ARG JUPYTERHUB_HUB_HELM_VERSION=4.3.5
FROM jupyterhub/k8s-hub:$JUPYTERHUB_HUB_HELM_VERSION AS release

# By default, the notebook base image is set to non-sudo user joyvan. This makes root-ful actions difficult.
USER root

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install --no-install-recommends -y \
    tzdata
RUN ln -fs /usr/share/zoneinfo/America/Alaska /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt install --no-install-recommends -y \
    python3 \
    python3-pip \
    less \
    vim \
    patch

RUN python3 --version
RUN python3 -m pip install --upgrade \
        awscli \
        pyyaml \
        boto3 \
        kubernetes \
        kubernetes_asyncio \
        opensarlab-backend==1.0.4 \
        --

# Generic Cluster-V2 setup
COPY ./shared/config.d/ /usr/local/etc/jupyterhub/jupyterhub_config.d/
COPY ./shared/templates/hub_home.html.j2 /usr/local/share/jupyterhub/templates/custom/page.html
COPY ./shared/python_overrides/portal_auth.py /tmp/site-packages/jupyterhub/portal_auth.py

# Lab specific setup
COPY geos631/hooks/geos631.sh /etc/user_server_includes/hooks/geos631.sh
COPY geos631/overrides/geos631.json /etc/user_server_includes/overrides/geos631.json

#COPY ./hub/web/usr/local/lib/jupyterhub/handlers/*.py /tmp/site-packages/jupyterhub/handlers/
RUN cp -r /tmp/site-packages/* /usr/local/lib/python*/site-packages

ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/osl

RUN mkdir -p -m 775 /usr/local/secrets && chown 1000:root /usr/local/secrets

USER jovyan


FROM release AS testing