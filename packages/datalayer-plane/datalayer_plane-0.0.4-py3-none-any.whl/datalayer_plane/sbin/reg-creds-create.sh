#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Creating the Registry Secrets"$NOCOLOR$NOBOLD
echo

for ns in datalayer-api datalayer-solr datalayer-system datalayer-jupyter datalayer-router datalayer-traefik datalayer-nginx
do
  echo Deleting reg-creds secret in namespace $ns
  kubectl delete secret reg-creds -n $ns
  echo Creating reg-creds secret in namespace $ns
  kubectl create secret \
    docker-registry reg-creds \
    -n $ns \
    --docker-server=$DATALAYER_DOCKER_REGISTRY_HOST \
    --docker-username=$DATALAYER_DOCKER_REGISTRY_USERNAME \
    --docker-password=$DATALAYER_DOCKER_REGISTRY_PASSWORD
  kubectl get secret reg-creds -n $ns -o jsonpath="{.data.\.dockerconfigjson}"
done
