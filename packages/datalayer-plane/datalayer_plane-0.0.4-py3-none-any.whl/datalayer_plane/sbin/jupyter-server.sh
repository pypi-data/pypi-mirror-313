#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Local Jupyter Server"$NOCOLOR$NOBOLD
echo

cd $DATALAYER_HOME/src/landings/datalayer/ui

yarn jupyter:server
