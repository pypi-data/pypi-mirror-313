#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Prometheus"$NOCOLOR$NOBOLD
echo

echo
echo open http://localhost:9090/prometheus/graph for Prometheus
echo

kubectl port-forward -n datalayer-observer service/datalayer-observer-kube-pr-prometheus 9090:9090 &
xdg-open http://localhost:9090/prometheus/graph

wait
