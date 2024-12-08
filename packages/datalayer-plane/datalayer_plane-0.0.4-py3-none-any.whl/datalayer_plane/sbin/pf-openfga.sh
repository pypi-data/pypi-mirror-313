#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to OpenFGA"$NOCOLOR$NOBOLD
echo

echo open http://localhost:8098/stores
echo open http://localhost:8098/stores/${DATALAYER_OPENFGA_STORE_ID}/authorization-models
echo

export POD_NAME=$(kubectl get pods --namespace datalayer-openfga -l "app.kubernetes.io/name=openfga,app.kubernetes.io/instance=datalayer-openfga" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace datalayer-openfga $POD_NAME -o jsonpath="{.spec.containers[0].ports[1].containerPort}")

kubectl --namespace datalayer-openfga port-forward $POD_NAME 8098:$CONTAINER_PORT
