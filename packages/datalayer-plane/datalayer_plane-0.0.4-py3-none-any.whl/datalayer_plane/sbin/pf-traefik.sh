#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Traefik Dashboard"$NOCOLOR$NOBOLD
echo

echo
echo open http://localhost:9000/dashboard/ for Traefik dashboard
echo

kubectl port-forward -n datalayer-traefik deployment/datalayer-traefik 9000:9000 &
xdg-open http://localhost:9000/dashboard/

wait
