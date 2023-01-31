ARG PYTHON_IMAGE=python:3.10.9-alpine
ARG APP_PORT=8000

# =====================================

FROM ${PYTHON_IMAGE}

WORKDIR /home/app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add libpq-dev jpeg-dev zlib-dev libjpeg

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE $APP_PORT

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
