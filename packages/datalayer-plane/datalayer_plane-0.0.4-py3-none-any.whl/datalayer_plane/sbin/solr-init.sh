#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Initialize Solr"$NOCOLOR$NOBOLD
echo

export SOLR_NAME=solr-datalayer
export NAMESPACE=datalayer-solr

cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: datalayer-solr-init
  namespace: datalayer-system
spec:
  containers:
  - name: datalayer-solr-init
    image: ${DATALAYER_DOCKER_REGISTRY_HOST}/datalayer/datalayer-solr:9.7.0
    imagePullPolicy: Always
    command: [ "/bin/sh", "-c", "--" ]
    args: [ "/opt/solr/create-collections-cloud.sh" ]
    env:
    - name: ZK_HOST
      value: "${SOLR_NAME}-solrcloud-zookeeper-headless.${NAMESPACE}.svc.cluster.local"
    - name: SOLR_HOST
      value: "${SOLR_NAME}-solrcloud-headless.${NAMESPACE}.svc.cluster.local"
    - name: SOLR_AUTH_TYPE
      value: "basic"
    - name: SOLR_AUTHENTICATION_OPTS
      value: "-Dbasicauth=solr:${DATALAYER_SOLR_PASSWORD}"
  restartPolicy: Never
  imagePullSecrets:
  - name: reg-creds
EOF

echo
echo -e $BOLD"Check the solr init pod."$NOBOLD
echo
echo kubectl get pod datalayer-solr-init -n datalayer-system -w

echo
echo -e $BOLD"Check the logs and once initialization successfully completed, delete the pod."$NOBOLD
echo
echo kubectl logs datalayer-solr-init -n datalayer-system -f

echo
echo -e $BOLD"Delete the init container."$NOBOLD
echo
echo kubectl delete pod datalayer-solr-init -n datalayer-system
echo
