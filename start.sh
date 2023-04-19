#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -d -p 8080:8080 \
  --name=${app} \
  -v $PWD:/app ${app}