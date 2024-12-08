#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Delete Service Pods"$NOCOLOR$NOBOLD
echo
echo -e $GREEN"Deleting pods in ${BOLD}datalayer-api${NOBOLD} namespace"$NOCOLOR
echo
kubectl delete pods -n datalayer-api -l app=iam
kubectl delete pods -n datalayer-api -l app=jupyter
kubectl delete pods -n datalayer-api -l app=library
kubectl delete pods -n datalayer-api -l app=manager
kubectl delete pods -n datalayer-api -l app=spacer
echo
echo -e $GREEN"Deleting pods in ${BOLD}datalayer-jupyter${NOBOLD} namespace"$NOCOLOR
echo
kubectl delete pods -n datalayer-jupyter -l app=operator
echo