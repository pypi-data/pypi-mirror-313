#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Telepresence"$NOCOLOR$NOBOLD

echo """
telepresence quit && telepresence connect --namespace datalayer

open http://datalayer-iam-svc:9700/api/iam/version
telepresence intercept datalayer-iam-iam --port 9700

open http://datalayer-library-svc:9800/api/library/version
telepresence intercept datalayer-library-library --port 9800

open http://datalayer-operator-svc:2111/api/operator/version
telepresence intercept datalayer-operator-operator --port 2111

open http://jupyter-router-svc:2000
open http://jupyter-router-api-svc:2001/api/routes
telepresence intercept jupyter-router-router --port 2000
telepresence intercept jupyter-router-api-svc --port 2001

open http://jupyterpool-svc:2300/api/jupyter-server?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
telepresence intercept jupyterpool-svc --port 2300

open http://solr-datalayer-solrcloud-headless:8983
curl http://solr-datalayer-solrcloud-zookeeper-headless:2181 # DATALAYER_SOLR_ZK_HOST
telepresence intercept solr-datalayer-solrcloud-headless --port 8983

ssh ...
telepresence intercept datalayer-jump-svc --port 2022

ssh ...
telepresence intercept datalayer-content-svc --port 2622
"""
