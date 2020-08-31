FROM continuumio/miniconda3


RUN apt-get update
RUN apt-get install libsndfile1 -y


ENV APP_ROOT /app/
ENV CONFIG_ROOT /config/

RUN mkdir ${CONFIG_ROOT}
RUN mkdir ${APP_ROOT}

ADD app/ ${APP_ROOT}

ADD /app/environment.yml ${CONFIG_ROOT}/environment.yml


RUN /opt/conda/bin/conda env create -f ${CONFIG_ROOT}/environment.yml

WORKDIR ${APP_ROOT}

ENTRYPOINT ["conda", "run", "-n", "audio_enviroment", "gunicorn", "--bind=0.0.0.0:5000","main:app"]
