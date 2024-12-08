#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Pushing Datalayer Docker Images"$NOCOLOR$NOBOLD
echo

source $PLANE_SBIN/docker.sh

do_push() {
  FILE=$1
  echo -e $WHITE_BCK"Pushing Docker image $BOLD[$FILE]$NOBOLD"$NOCOLOR
  echo
  cd $PLANE_HOME/etc/dockerfiles/$FILE && \
    make push
  if [ $? -eq 0 ]
  then
    echo
    echo -e $BOLD$GREEN"Docker image push [${FILE}] SUCCESS"$NOCOLOR$NOBOLD
  else
    echo
    echo -e $BOLD$RED"Docker image push [${FILE}] FAILURE"$NOCOLOR$NOBOLD
    echo
    exit
  fi
  echo
}

push() {
  if [ -z "$1" ]; then
    for DOCKER_FILE in "${DOCKER_FILES[@]}"
    do
      do_push $DOCKER_FILE
    done
  else
    build $1
  fi
}

push

: <<'EOC'
source docker

for DOCKERIMAGE in "${DOCKER_IMAGES[@]}"
do
  echo
  echo -e $BOLD"Pushing $DOCKERIMAGE..."$NOBOLD
  docker push $DOCKERIMAGE
  if [ $? -eq 0 ]
  then
    echo
    echo -e $BOLD$GREEN"Push of docker image [${DOCKERFILE%/}] is successful."$NOCOLOR$NOBOLD
  else
    echo
    echo -e $BOLD$RED"Push of docker image [${DOCKERFILE%/}] failed..."$NOCOLOR$NOBOLD
    echo
    exit
  fi
  echo
done
EOC

# Push Datalayer Kernels base image.
# cd $PLANE_HOME/../kernels && \
#   make push-jupyter-kernel-python