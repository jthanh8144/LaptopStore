ARG PYTHON_IMAGE=python:3.10.6-slim-bullseye
ARG APP_PORT=8000

# =====================================

FROM ${PYTHON_IMAGE}

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE $APP_PORT

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
