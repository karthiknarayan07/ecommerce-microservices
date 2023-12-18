#!/bin/bash

BASE_DIR=$(pwd)

for SERVICE_DIR in $BASE_DIR/*/; do
  if [ -f "${SERVICE_DIR}Dockerfile" ]; then
    cd "$SERVICE_DIR" || exit

    git pull origin master

    cd "$BASE_DIR" || exit
  fi
done

docker compose build
docker compose up
