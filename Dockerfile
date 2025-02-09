FROM python:3.8.10

#Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

#Setup workdir
WORKDIR /app

COPY ./pyproject.toml  ./pyproject.toml
COPY ./poetry.lock  ./poetry.lock
COPY ./de_neobank_frontend  ./neobank_gold

RUN apt-get update \
    && apt-get -y upgrade \
    && pip3 install --no-cache-dir poetry \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8501

ENTRYPOINT [ "poetry", "run" ]
