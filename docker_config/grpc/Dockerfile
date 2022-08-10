FROM auth_app
WORKDIR /opt/auth/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/opt/auth
EXPOSE 5005

ADD ./requirements_grpc.txt ./requirements.txt
ADD src/grpc_app /opt/auth/grpc_app
ADD src/app /opt/auth/app

RUN apk add --update  --no-cache libstdc++ libc6-compat openssh-client git gcc cython linux-headers make musl-dev python3-dev g++
RUN pip install --upgrade pip \
  && pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3",  "grpc_app/server.py"]