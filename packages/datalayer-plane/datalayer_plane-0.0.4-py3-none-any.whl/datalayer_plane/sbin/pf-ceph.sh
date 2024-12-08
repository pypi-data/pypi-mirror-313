#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Ceph Dashboard"$NOCOLOR$NOBOLD
echo

echo
echo open http://localhost:7000/ for Ceph dashboard
echo
echo Command to get the admin password
echo kubectl -n datalayer-storage get secret rook-ceph-dashboard-password -o jsonpath=\"{[\'data\'][\'password\']}\" \| base64 --decode \&\& echo
echo

kubectl port-forward -n datalayer-storage service/rook-ceph-mgr-dashboard 7000:7000 &
xdg-open http://localhost:7000/

wait
