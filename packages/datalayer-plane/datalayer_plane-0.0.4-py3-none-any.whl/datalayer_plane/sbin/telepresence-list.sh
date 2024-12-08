#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Telepresence Install"$NOCOLOR$NOBOLD
echo

telepresence status
echo

telepresence connect --namespace datalayer
echo

telepresence list
