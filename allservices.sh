#!/bin/bash

BASE_DIR=$(pwd)

for SERVICE_DIR in $BASE_DIR/*/; do
  if [ -f "${SERVICE_DIR}Dockerfile" ]; then
    cd "$SERVICE_DIR" || exit

    sudo git pull origin master

    cd "$BASE_DIR" || exit
  fi
done

sudo docker compose build
sudo docker compose up
