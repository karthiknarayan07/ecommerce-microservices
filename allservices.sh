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


# Note:- 
# This shell file is used to build all services and run them in docker compose, 
# cosnidering every folder has separate git repo, we need to pull the latest code from git repo before building the docker image.
# This shell file will be executed by jenkins job when implementing CI/CD pipeline.