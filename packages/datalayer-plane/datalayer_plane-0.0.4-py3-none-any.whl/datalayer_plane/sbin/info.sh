#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Plane Information"$NOCOLOR$NOBOLD
echo

echo DATALAYER_RUN_HOST: $DATALAYER_RUN_HOST
echo
echo KUBECONFIG: $KUBECONFIG
echo
kubectl config view
echo
