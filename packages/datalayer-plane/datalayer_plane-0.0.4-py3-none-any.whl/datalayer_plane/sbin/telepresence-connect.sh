#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Telepresence Connect"$NOCOLOR$NOBOLD

echo
telepresence quit
echo
telepresence connect --namespace datalayer
