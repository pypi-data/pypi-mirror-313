#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Telepresence Install"$NOCOLOR$NOBOLD

# https://www.telepresence.io/docs/latest/quick-start

echo """
curl -ik https://kubernetes.default.svc.default.local # Should return 403.

telepresence helm install

telepresence quit
telepresence connect --namespace datalayer
curl http://datalayer-iam-svc.datalayer:9700/api/iam/version
open http://datalayer-iam-svc.datalayer:9700/api/iam/version
"""

echo """
telepresence status
telepresence list
telepresence intercept datalayer-iam --port 9700:9700 -n datalayer
open http://127.0.0.1:9700/api/iam/version
telepresence leave datalayer-iam
telepresence quit
"""
