#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Prepulling Docker Images on CPU Kubernetes Nodes"$NOCOLOR$NOBOLD
echo

# Pre-pull CPU Docker images.
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: images-prepuller-cpu
  namespace: datalayer-jupyter
spec:
  selector:
    matchLabels:
      name: prepuller
  template:
    metadata:
      labels:
        name: prepuller
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: role.datalayer.io/jupyter
                operator: In
                values:
                - 'true'
              - key: xpu.datalayer.io/cpu
                operator: In
                values:
                - 'true'
      imagePullSecrets:
        - name: reg-creds
      initContainers:
        - name: prepuller-network-tools
          image: quay.io/jupyterhub/k8s-network-tools:3.3.7
          imagePullPolicy: Always
          command: ["sh", "-c", "'true'"]
        - name: prepuller-jupyter-companion
          image: ${DATALAYER_DOCKER_REGISTRY}/jupyter-companion:0.0.6
          imagePullPolicy: Always
          command: ["sh", "-c", "'true'"]
        - name: prepuller-python
          image: ${DATALAYER_DOCKER_REGISTRY}/jupyter-python:0.0.8
          imagePullPolicy: Always
          command: ["sh", "-c", "'true'"]
#        - name: prepuller-youtube
#          image: ${DATALAYER_DOCKER_REGISTRY}/jupyter-youtube:0.0.8
#          imagePullPolicy: Always
#          command: ["sh", "-c", "'true'"]
      containers:
        - name: pause
          image: gcr.io/google_containers/pause
EOF

kubectl get daemonset images-prepuller-cpu -n datalayer-jupyter

echo
echo -e $BOLD$BLUE_BCK"kubectl get pods -l name=prepuller -n datalayer-jupyter"$NOCOLOR$NOBOLD
echo
echo -e $BOLD$BLUE_BCK"kubectl delete daemonset images-prepuller-cpu -n datalayer-jupyter"$NOCOLOR$NOBOLD
echo

kubectl get pods -l name=prepuller -n datalayer-jupyter -w
