# OpenScienceLab custom lab images

* [GEOS631](./geos631) - Foundations of Geophysics 
* [GEOS636](./geos636) - Programming and Automation for Geosciences

## Running lab images locally

```shell
lab=geos631;

docker \
     run \
     -it \
     -p 8888:8888 \
     --entrypoint bash \
     ghcr.io/asfopensarlab/${lab}:test \
         -c " \
               /etc/user_server_includes/hooks/${lab}.sh &&  \
               tini -g -- start.sh start-notebook.py \
            "
```