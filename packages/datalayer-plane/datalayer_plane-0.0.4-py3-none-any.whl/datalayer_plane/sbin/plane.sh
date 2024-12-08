#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

export PLANE_SBIN="$( cd "$( dirname "$0" )" && pwd )"

export PLANE_HOME=$(realpath $PLANE_SBIN/../..)

INITIAL_PATH=$PATH

export PATH=$PLANE_SBIN:$PATH

source $PLANE_SBIN/cli.sh

$PLANE_SBIN/header.sh "$@"

# if [ $# == 0 ] ; then
#   exit 0;
# fi

$PLANE_SBIN/$1 "${@:2}"
FLAG=$?

PATH=$INITIAL_PATH

exit $FLAG
