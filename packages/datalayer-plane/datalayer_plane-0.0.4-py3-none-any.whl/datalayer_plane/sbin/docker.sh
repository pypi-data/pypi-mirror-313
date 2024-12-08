#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

declare -a DOCKER_FILES=(
  "datalayer-iam"
  "datalayer-jupyter"
  "datalayer-jupyter-companion"
  "datalayer-library"
  "datalayer-mailer"
  "datalayer-manager"
  "datalayer-operator"
  "datalayer-solr"
  "datalayer-spacer"
  "ingress-nginx-controller"
  "jupyter-python"
  "whoami"
#  "datalayer-jump"
#  "example-simple"
#  "example-tornado"
#  "jupyter-fastai-cuda"
#  "jupyter-python-cuda"
#  "jupyter-pytorch-cuda"
#  "jupyter-rapids-cuda"
#  "kubectl"
  )

declare -a DOCKER_IMAGES=(
  "datalayer/datalayer-iam:latest"
  "datalayer/datalayer-jupyter-companion:latest"
  "datalayer/datalayer-jupyter:latest"
  "datalayer/datalayer-library:latest"
  "datalayer/datalayer-operator:latest"
  "datalayer/datalayer-solr:latest"
  "datalayer/datalayer-spacer:latest"
  "datalayer/jupyter-python:latest"
#  "datalayer/datalayer-jump:0.0.6"
#  "datalayer/kubectl:0.0.6"
)
