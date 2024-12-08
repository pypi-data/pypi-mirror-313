#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

if [ "$DATALAYER_PLANE_SHOW_HEADER" == "false" ]
then
  exit 0
fi

if [ "$DATALAYER_PLANE_SKIP_HEADER" == "true" ]
then
  exit 0
fi

echo -e $GREEN$BOLD"""┏┓┓ ┏┓┳┓┏┓
┃┃┃ ┣┫┃┃┣ 
┣┛┗┛┛┗┛┗┗┛

Copyright (c) Datalayer, Inc. https://datalayer.io"""
echo -e $NOBOLD$NOCOLOR
