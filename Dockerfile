FROM python:3.9-slim-buster

# https://pythonspeed.com/articles/pipenv-docker/
# Alternative: https://medium.com/swlh/setting-up-a-secure-django-project-repository-with-docker-and-django-environ-4af72ce037f0
RUN pip install pipenv

COPY Pipfile* /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
