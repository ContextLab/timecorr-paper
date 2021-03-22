FROM continuumio/miniconda


COPY environment.yml .
RUN \
   conda env update -n root -f environment.yml \
&& conda clean -a



# Make sure the environment is activated:
RUN echo "Make sure hypertools is installed:"
RUN python -c "import hypertools"

RUN pip install --upgrade --ignore-installed \
git+git://github.com/FIU-Neuro/brainconn.git \
git+git://github.com/lucywowen/timecorr-1.git@spot_check

# Make sure the environment is activated:
RUN echo "Make sure timecorr is installed:"
RUN python -c "import timecorr"


# The code to run when container is started:
COPY run.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "timecorr_env_spotcheck", "python", "run.py"]