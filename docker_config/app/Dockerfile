FROM python:3.9.6-alpine
WORKDIR /opt/auth
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/opt/auth

ADD src/app /opt/auth/app
ADD src/runserver.py /opt/auth/
ADD src/pywsgi.py /opt/auth/
ADD src/migrations /opt/auth/migrations
ADD ./requirements.txt ./

RUN apk add build-base && apk add  libffi-dev \
  && pip install --upgrade pip \
  && pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "pywsgi.py"]
