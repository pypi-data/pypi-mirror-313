#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Planes"$NOCOLOR$NOBOLD
echo

helm ls --all-namespaces
