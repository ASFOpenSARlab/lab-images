# 2026-05-04 is JupyterLab v4.5.7
# https://quay.io/repository/jupyter/base-notebook?tab=tags
FROM quay.io/jupyter/base-notebook:2026-05-04 AS release

# Base Stage ****************************************************************
USER root
WORKDIR /

RUN set -ve

# ignore DL3059 to make the two codeblocks distinct
# ignore DL3009 since deleting apt-get lists makes later installs fail
# hadolint ignore=DL3009,DL3059
RUN apt-get update
# ignore DL3008 because pinning is not desired
# ignore DL3009 since deleting apt-get lists makes later installs fail
# hadolint ignore=DL3008,DL3009
RUN apt-get install --no-install-recommends -y \
        software-properties-common \
        git && \
    apt-get install --no-install-recommends -y gpg-agent && \
    add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update && \
    apt-get upgrade -y

# ignore DL3008 because pinning is not desired
# hadolint ignore=DL3008
RUN apt-get install --no-install-recommends --fix-missing -y \
    ### GENERAL
    zip \
    unzip \
    wget \
    vim \
    rsync \
    less \
    snaphu \
    curl \
    ca-certificates \
    openssh-client \
    libglx-mesa0 \
    emacs \
    gnupg2 \
    jq \
    gfortran \
    make \
    proj-bin \
    geotiff-bin \
    libshp-dev \
    libshp4 \
    libhdf5-dev \
    libnetcdf-dev \
    libgdal-dev \
    libgsl-dev \
    gdal-bin \
    ### SNAP
    default-jdk-headless \
    ### Install texlive for PDF exporting of notebooks containing LaTex
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    ### PyGMTSAR
    csh \
    autoconf \
    make \
    libtiff5-dev \
    liblapack-dev \
    libgmt-dev \
    gmt-dcw \
    gmt-gshhg \
    gmt \
    --

# ignore DL3059 to make the two codeblocks distinct
# hadolint ignore=DL3059
RUN mamba install -c conda-forge -y \
    ### Install plotting and general
    awscli \
    boto3 \
    pyyaml \
    bokeh \
    plotly \
    'pyopenssl>=23.0.0' \
    zstandard==0.25.0

# hadolint ignore=DL3059
RUN mamba install -c conda-forge -y \
    ### Install jupyter libaries
    kernda \
    jupyter-resource-usage \
    nb_conda_kernels \
    jupyterlab-spellchecker \
    ipympl \
    jupyterlab-h5web \
    jupyterlab_widgets \
    ipywidgets \
    #jupyter-ai \
    jupyterlab-git \
    # Coordinate with cluster dependency versions
    'jupyterhub>=5.4.6' \
    'jupyter_server>=2.18.0' \
    panel

# hadolint ignore=DL3059
RUN mamba install -c conda-forge -y \
    ### Dask
    dask-gateway \
    dask \
    distributed \
    ipyleaflet \
    'jupyter-collaboration>=4.4.0' \
    'jupyter-collaboration-ui>=2.4.0' \
    jupytergis \
    --

# ignore DL3059 to make the two codeblocks distinct
# ignore DL3013 since pinning packages is not desired
# hadolint ignore=DL3013,DL3059
RUN python3 -m pip install --no-cache-dir  \
    ### For ASF
    url-widget \
    opensarlab-frontend==1.5.4 \
    jb-toc \
    nbgitpuller-jl-interface==1.1.1 \
    opensciencelab-tours==0.3.2 \
    mystmd \
    jupyterlab_myst \
    playwright \
    ### For pyGMTSAR
    pygmtsar

RUN jupyter labextension disable @jupyter/collaboration-extension

ENV PIXI_HOME=/usr/local/pixi
RUN set -eux; \
    mkdir -p "${PIXI_HOME}"; \
    curl -fsSL https://pixi.sh/install.sh | bash; \
    mv -v "${PIXI_HOME}/bin/pixi" /usr/local/bin/pixi; \
    chmod 0755 /usr/local/bin/pixi; \
    pixi --version
# reset PIXI_HOME to location on persistent volume after install for storing workspaces.toml
ENV PIXI_HOME=/home/jovyan/.pixi

WORKDIR /

RUN mkdir -p /tmp/build/GMTSAR /usr/local/GMTSAR &&\
    git clone --branch master https://github.com/gmtsar/gmtsar /tmp/build/GMTSAR/

WORKDIR /tmp/build/GMTSAR

RUN autoconf &&\
    ./configure --with-orbits-dir=/tmp CFLAGS='-z muldefs' LDFLAGS='-z muldefs' &&\
    make &&\
    make install &&\
    mv -v /tmp/build/GMTSAR/bin /usr/local/GMTSAR/bin &&\
    rm -rf /tmp/build

WORKDIR /

### Extra stuff
# Make sure that any files in the home directory are jovyan permission
RUN chown -R jovyan:users "$HOME/" &&\
    # Make sure mamba (within conda) has write access
    chmod -R 777 /opt/conda/pkgs/ &&\
    # Make sure JupyterLab settings is writable
    mkdir -p /opt/conda/share/jupyter/lab/settings/ &&\
    chown jovyan:users /opt/conda/share/jupyter/lab/settings/ &&\
    chmod -R 775 /opt/conda/share/jupyter/lab/settings/ &&\
    # Add sudo group user 599 elevation
    addgroup -gid 599 elevation &&\
    echo '%elevation ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers &&\
    # Use the kernel display name `base` for the base conda environment
    mamba run -n base kernda --display-name base -o /opt/conda/share/jupyter/kernels/python3/kernel.json &&\
    mamba clean -y --all &&\
    mamba shell init -s bash --root-prefix=/opt/conda/ &&\
    rm -rf /home/jovyan/..?* /home/jovyan/.[!.]* /home/jovyan/*

# Stage 2: Squash everything into a single layer
FROM scratch
COPY --from=release / /

### GMTSAR
ENV PATH=/usr/local/GMTSAR/bin:$PATH

# reset PIXI_HOME to location on persistent volume after install for storing workspaces.toml
ENV PIXI_HOME=/home/jovyan/.pixi

WORKDIR /home/jovyan
USER jovyan
