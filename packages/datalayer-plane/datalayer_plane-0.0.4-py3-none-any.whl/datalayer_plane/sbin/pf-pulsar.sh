#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Pulsar Broker"$NOCOLOR$NOBOLD
echo

echo
echo Connect to http://localhost:6650 for Pulsar Broker
echo
echo Read more on https://datalayer.tech/docs/build/kubernetes/services/system/pulsar
echo

kubectl port-forward -n datalayer-pulsar service/datalayer-pulsar-broker 6650:6650
