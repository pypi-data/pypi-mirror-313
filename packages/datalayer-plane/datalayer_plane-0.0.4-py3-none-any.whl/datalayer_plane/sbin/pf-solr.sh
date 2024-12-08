#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Solr"$NOCOLOR$NOBOLD
echo

echo
echo open http://localhost:8983 for Solr
echo open http://localhost:2181 for Solr Zookeeper
echo

kubectl port-forward -n datalayer-solr service/solr-datalayer-solrcloud-zookeeper-client 2181:2181 &

kubectl port-forward -n datalayer-solr service/solr-datalayer-solrcloud-headless 8983:8983 &

wait
