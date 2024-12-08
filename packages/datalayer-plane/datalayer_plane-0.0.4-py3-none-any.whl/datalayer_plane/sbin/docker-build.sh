#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Building Datalayer Docker Images"$NOCOLOR$NOBOLD
echo

source $PLANE_SBIN/docker.sh

build() {
  FILE=$1
  echo -e $WHITE_BCK"Building Docker image $BOLD[$FILE]$NOBOLD"$NOCOLOR
  echo
  cd $PLANE_HOME/etc/dockerfiles/$FILE && \
    make build
  if [ $? -eq 0 ]
  then
    echo
    echo -e $BOLD$GREEN"Docker image build [$YELLOW${FILE}$GREEN] SUCCESS"$NOCOLOR$NOBOLD
  else
    echo
    echo -e $BOLD$RED"Docker image build [$YELLOW${FILE}$GREEN] FAILURE"$NOCOLOR$NOBOLD
    echo
    exit
  fi
  echo
}

if [ -z "$1" ]; then
  for DOCKER_FILE in "${DOCKER_FILES[@]}"
  do
    build $DOCKER_FILE
  done
else
  build $1
fi

# Build Datalayer Kernels base image.
# cd $PLANE_HOME/../kernels && \
#   rm -fr build .image-jupyter-kernel-* && \
#   make jupyter-kernel-python
