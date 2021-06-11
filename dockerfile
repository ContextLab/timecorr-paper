FROM ubuntu:bionic

LABEL maintainer="Contextual Dynamics Lab <contextualdynamics@gmail.com>"

ARG DEBIAN_FRONTEND=noninteractive
ARG WORKDIR="/mnt"
ARG NOTEBOOK_IP=0.0.0.0
ARG PORT=9999

ENV LANG=C.UTF-8 \
    PATH="/opt/conda/bin:$PATH" \
    NOTEBOOK_DIR=$WORKDIR \
    NOTEBOOK_IP=$NOTEBOOK_IP \
    NOTEBOOK_PORT=$PORT

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc \
    && apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends eatmydata \
    && eatmydata apt-get install -y --no-install-recommends \
        bzip2 \
        ca-certificates \
        curl \
        gcc \
        git \
        libfontconfig1-dev \
        libgl1-mesa-glx -y \
        mpich \
        pkg-config \
        sudo \
        swig \
        vim \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && conda config --set auto_update_conda false \
    && conda config --set notify_outdated_conda false \
    && conda install -y \
        _libgcc_mutex=0.1=main \
        blas=1.0=mkl \
        ca-certificates=2019.5.15=1 \
        certifi=2019.6.16=py36_1 \
        ipykernel=5.3.4 \
        ipython=7.16.1 \
        ipywidgets=7.5.1 \
        jinja2=2.11.2 \
        libedit=3.1.20181209=hc058e9b_0 \
        libffi=3.2.1=hd88cf55_4 \
        libgcc-ng=8.2.0=hdf63c60_1 \
        libgfortran-ng=7.3.0=hdf63c60_0 \
        libstdcxx-ng=8.2.0=hdf63c60_1 \
        mkl-service=2.0.2=py36h7b6447c_0 \
        mkl_fft=1.0.12=py36ha843d7b_0 \
        mkl_random=1.0.2=py36hd81dba3_0 \
        nbconvert=5.6.1 \
        nbformat=5.0.7 \
        ncurses=6.1=he6710b0_1 \
        notebook=6.1.4 \
        numpy-base=1.16.4=py36hde5b4d6_0 \
        openssl=1.1.1c=h7b6447c_1 \
        pandoc=2.10 \
        pip=19.0.3=py36_0 \
        prometheus_client=0.8.0 \
        python=3.6.8=h0371630_0 \
        pyzmq=19.0.2 \
        readline=7.0=h7b6447c_5 \
        setuptools=40.8.0=py36_0 \
        sqlite=3.27.2=h7b6447c_0 \
        terminado=0.9.1 \
        tk=8.6.8=hbc83047_0 \
        tornado=6.0.4 \
        traitlets=4.3.3 \
        wheel=0.33.1=py36_0 \
        widgetsnbextension=3.5.1 \
        xz=5.2.4=h14c3975_4 \
        zlib=1.2.11=h7b6447c_3 \
    && conda clean -tipsy \
    && pip install \
        alabaster==0.7.12 \
        babel==2.6.0 \
        biopython==1.74 \
        chardet==3.0.4 \
        citeproc-py==0.4.0 \
        cycler==0.10.0 \
        deepdish==0.3.6 \
        docutils==0.14 \
        duecredit==0.7.0 \
        future==0.17.1 \
        hypertools==0.5.1 \
        idna==2.8 \
        imagesize==1.1.0 \
        intel-openmp==2019.0 \
        jinja2==2.10 \
        jupyter_contrib_nbextensions==0.5.1 \
        kiwisolver==1.0.1 \
        llvmlite==0.28.0 \
        lxml==4.3.3 \
        markupsafe==1.1.1 \
        matplotlib==3.0.3 \
        mkl==2019.0 \
        mock==2.0.0 \
        neurosynth==0.3.8 \
        nibabel==2.5.0 \
        nose==1.3.7 \
        numba==0.43.1 \
        numexpr==2.6.9 \
        numpy==1.16.2 \
        packaging==19.0 \
        pandas==0.24.2 \
        pbr==5.1.3 \
        ply==3.11 \
        ppca==0.0.4 \
        pygments==2.3.1 \
        pyparsing==2.3.1 \
        python-dateutil==2.8.0 \
        pytz==2018.9 \
        requests==2.21.0 \
        scikit-learn==0.19.2 \
        scipy==1.2.1 \
        seaborn==0.9.0 \
        six==1.12.0 \
        snowballstemmer==1.2.1 \
        sphinx==2.0.0 \
        sphinxcontrib-applehelp==1.0.1 \
        sphinxcontrib-devhelp==1.0.1 \
        sphinxcontrib-htmlhelp==1.0.1 \
        sphinxcontrib-jsmath==1.0.1 \
        sphinxcontrib-qthelp==1.0.2 \
        sphinxcontrib-serializinghtml==1.1.3 \
        tables==3.5.1 \
        umap-learn==0.3.8 \
        urllib3==1.24.1 \
        git+git://github.com/lucywowen/timecorr-1.git@spot_check \
        git+https://github.com/FIU-Neuro/brainconn.git \
    && rm -rf ~/.cache/pip \
    && jupyter nbextension enable --py widgetsnbextension --sys-prefix \
    && jupyter notebook --generate-config \
    && ipython profile create \
    &&  sed -i \
        -e 's/^# c.Completer.use_jedi = True/c.Completer.use_jedi = False/' \
        -e 's/^#c.Completer.use_jedi = True/c.Completer.use_jedi = False/' \
        -e 's/^# c.IPCompleter.use_jedi = True/c.IPCompleter.use_jedi = False/' \
        ~/.ipython/profile_default/ipython_config.py \
    && mkdir -p /root/.jupyter \
    && echo "from os import getenv" > /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.ip = getenv(\"NOTEBOOK_IP\")" >> /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.port = int(getenv(\"NOTEBOOK_PORT\"))" >> /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.notebook_dir = getenv(\"NOTEBOOK_DIR\")" >> /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.FileContentsManager.delete_to_trash = False" >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR $WORKDIR
