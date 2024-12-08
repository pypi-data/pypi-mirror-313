#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Pulling Datalayer Docker Images"$NOCOLOR$NOBOLD
echo

source docker

for DOCKERIMAGE in "${DOCKER_IMAGES[@]}"
do
  echo
  echo -e $BOLD"Pulling $DOCKERIMAGE..."$NOBOLD
  docker pull $DOCKERIMAGE
  echo
done
