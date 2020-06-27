FROM python:3.8.3-alpine
COPY . /app
WORKDIR /app
RUN apk update
RUN apk add gcc
RUN apk add libc-dev
RUN apk add libffi-dev
RUN apk add openssl-dev
RUN pip3 install -r python-dependencies.txt
EXPOSE 2424/tcp
CMD ["python", "api.py"]