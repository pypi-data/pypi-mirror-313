#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Vault"$NOCOLOR$NOBOLD
echo

echo open http://localhost:8200
echo

kubectl port-forward datalayer-vault-0 8200:8200 -n datalayer-vault
