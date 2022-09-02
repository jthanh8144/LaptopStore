ARG PYTHON_IMAGE=python:3.10.6-slim-bullseye
ARG APP_PORT=8000

# =====================================

FROM ${PYTHON_IMAGE}

WORKDIR /home/app

# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc

RUN apt-get update && apt-get install -y \
    python-dev python-setuptools \
    libtiff-dev libxml2-dev libxslt1-dev \
    libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev python-tk \
    libpq-dev gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE $APP_PORT

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
