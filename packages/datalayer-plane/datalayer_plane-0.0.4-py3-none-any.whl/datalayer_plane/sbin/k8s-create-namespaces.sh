#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Create Kubernetes Namespaces"$NOCOLOR$NOBOLD
echo

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-api
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-storage
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-cuda-operator
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-jupyter
#  labels:
#    observer.datalayer.io/prometheus: "true"
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-nginx
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-openfga
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-pulsar
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-router
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-solr
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-solr-operator
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-system
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-traefik
---
apiVersion: v1
kind: Namespace
metadata:
  name: datalayer-vault
EOF
