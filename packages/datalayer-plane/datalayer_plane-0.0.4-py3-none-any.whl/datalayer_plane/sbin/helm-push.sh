#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Pushing Datalayer Helm Charts"$NOCOLOR$NOBOLD
echo

cd $PLANE_HOME/etc/helm/charts

for HELM_CHART in iam jupyter operator
do
    echo -----------------------------------------------
    echo -e "Packaging Helm Chart [datalayer-$HELM_CHART]"
    echo
    rm *.tgz || true
    helm package datalayer-$HELM_CHART
    echo
    echo -e "Pushing Helm Chart [datalayer-$HELM_CHART]"
    helm push *.tgz oci://$DATALAYER_HELM_REGISTRY
    rm *.tgz || true
    echo
done
