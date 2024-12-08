#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Removing Datalayer Plane"$NOCOLOR$NOBOLD
echo

function kubernetes_telepresence() {
  export RELEASE=kubernetes-telepresence
  export NAMESPACE=ambassador
  helm delete $RELEASE --namespace $NAMESPACE
}

function kubernetes_dashboard() {
  export RELEASE=kubernetes-dashboard
  export NAMESPACE=kube-system
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_nginx() {
  export RELEASE=datalayer-nginx
  export NAMESPACE=datalayer-nginx
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_traefik() {
  export RELEASE=datalayer-traefik
  export NAMESPACE=datalayer-traefik
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ceph_operator() {
  export RELEASE=datalayer-ceph-operator
  export NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ceph_cluster() {
  export RELEASE=datalayer-ceph-cluster
  export NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_shared_filesystem() {
  export RELEASE=datalayer-shared-filesystem
  export NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_cert_manager() {
  export RELEASE=datalayer-cert-manager
  export NAMESPACE=datalayer-cert-manager
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_datashim() {
  export RELEASE=datalayer-datashim
  export NAMESPACE=datalayer-datashim
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_cuda_operator() {
  export RELEASE=datalayer-cuda-operator
  export NAMESPACE=datalayer-cuda-operator
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_solr_operator() {
  export RELEASE=datalayer-solr-operator
  export NAMESPACE=datalayer-solr-operator
  helm delete $RELEASE --namespace $NAMESPACE
  kubectl delete \
    -n $NAMESPACE \
    -f https://solr.apache.org/operator/downloads/crds/v0.8.0/all-with-dependencies.yaml
}

function datalayer_config() {
  export RELEASE=datalayer-config
  export NAMESPACE=datalayer-config
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_mailer() {
  export RELEASE=datalayer-mailer
  export NAMESPACE=datalayer-system
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_vault() {
  export RELEASE=datalayer-vault
  export NAMESPACE=datalayer-vault
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_pulsar() {
  export RELEASE=datalayer-pulsar
  export NAMESPACE=datalayer-pulsar
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ldap() {
  export RELEASE=datalayer-ldap
  export NAMESPACE=datalayer-ldap
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ldapadmin() {
  export RELEASE=datalayer-ldap
  export NAMESPACE=datalayer-ldap
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_keycloak() {
  export RELEASE=datalayer-keycloak
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_observer() {
  export RELEASE=datalayer-observer
  export NAMESPACE=datalayer-observer
  helm delete $RELEASE --namespace $NAMESPACE
  echo 
  echo You will need to remove manually the CR opentelemetry.io/v1beta1/opentelemetrycollectors.
  echo To achieve that you will need to remove manually the finalizer on them.
  echo Once the CR is removed, the associated resources should be released.
  echo 
}

function datalayer_manager() {
  export RELEASE=datalayer-manager
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_iam() {
  export RELEASE=datalayer-iam
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_operator() {
  export RELEASE=datalayer-operator
  export NAMESPACE=datalayer-jupyter
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_openfga() {
  export RELEASE=datalayer-openfga
  export NAMESPACE=datalayer-openfga
#  --no-hooks
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_spacer() {
  export RELEASE=datalayer-spacer
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_library() {
  export RELEASE=datalayer-library
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_jupyter() {
  export RELEASE=datalayer-jupyter
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyterhub() {
  export RELEASE=jupyterhub
  export NAMESPACE=jupyterhub
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_jump() {
  export RELEASE=datalayer-jump
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_content() {
  export RELEASE=datalayer-content
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_minio() {
  export RELEASE=datalayer-minio
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
#  kubectl minio tenant delete $RELEASE -n $NAMESPACE
#  kubectl minio delete
#  kubectl delete namespace $NAMESPACE
}

function datalayer_editor() {
  export RELEASE=datalayer-editor
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyterpool() {
  export RELEASE=jupyterpool
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyter_server() {
  export RELEASE=jupyter-server
  export NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyter_editor() {
  export RELEASE=jupyter-editor
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function example_simple() {
  export RELEASE=example-simple
  export NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function commands() {
  echo -e $YELLOW"💛  Valid commands: [ datalayer-cert-manager | datalayer-datashim | datalayer-operator | datalayer-mailer | datalayer-openfga | datalayer-cuda-operator | datalayer-solr-operator | datalayer-config | datalayer-vault | datalayer-pulsar | kubernetes-dashboard | datalayer-ldap | datalayer-ldapadmin | datalayer-keycloak | datalayer-iam | datalayer-manager | datalayer-spacer | datalayer-library | datalayer-run | datalayer-nginx | datalayer-traefik | jupyterhub | jupyterpool | jupyter-server | jupyter-editor | datalayer-minio | datalayer-jump | datalayer-content | datalayer-editor | example-simple | example-simple ]"$NOCOLOR 1>&2
}

CMDS="$1"

if [ -z "$CMDS" ]; then
  echo -e $RED$BOLD"💔  No command to execute has been provided."$NOCOLOR$NOBOLD 1>&2
  echo
  exit 1
fi

function apply_cmd() {

  echo -e $BOLD"✋  Removing [$BLUE$1$NOCOLOR]"$NOBOLD
  echo

  case "$1" in

    kubernetes-telepresence)
      kubernetes_telepresence
      ;;

    kubernetes-dashboard)
      kubernetes_dashboard
      ;;

    datalayer-nginx)
      datalayer_nginx
      ;;

    datalayer-traefik)
      datalayer_traefik
      ;;

    datalayer-ceph-operator)
      datalayer_ceph_operator
      ;;

    datalayer-ceph-cluster)
      datalayer_ceph_cluster
      ;;

    datalayer-shared-filesystem)
      datalayer_shared_filesystem
      ;;

    datalayer-cert-manager)
      datalayer_cert_manager
      ;;

    datalayer-mailer)
      datalayer_mailer
      ;;

    datalayer-datashim)
      datalayer_datashim
      ;;

    datalayer-cuda-operator)
      datalayer_cuda_operator
      ;;

    datalayer-solr-operator)
      datalayer_solr_operator
      ;;

    jupyterpool)
      jupyterpool
      ;;

    jupyter-server)
      jupyter_server
      ;;

    jupyter-editor)
      jupyter_editor
      ;;

    datalayer-config)
      datalayer_config
      ;;

    datalayer-vault)
      datalayer_vault
      ;;

    datalayer-pulsar)
      datalayer_pulsar
      ;;

    datalayer-ldap)
      datalayer_ldap
      ;;

    datalayer-ldapadmin)
      datalayer_ldapadmin
      ;;

    datalayer-keycloak)
      datalayer_keycloak
      ;;

    datalayer-observer)
      datalayer_observer
      ;;

    datalayer-manager)
      datalayer_manager
      ;;

    datalayer-iam)
      datalayer_iam
      ;;

    datalayer-operator)
      datalayer_operator
      ;;

    datalayer-openfga)
      datalayer_openfga
      ;;

    datalayer-spacer)
      datalayer_spacer
      ;;

    datalayer-library)
      datalayer_library
      ;;

    datalayer-jupyter)
      datalayer_jupyter
      ;;

    jupyterhub)
      jupyterhub
      ;;

    datalayer-minio)
      datalayer_minio
      ;;

    datalayer-jump)
      datalayer_jump
      ;;

    datalayer-content)
      datalayer_content
      ;;

    datalayer-editor)
      datalayer_editor
      ;;

    example-simple)
      example_simple
      ;;

    *)
      echo -e $RED$BOLD"💔  Unknown command: $1"$NOBOLD$NOCOLOR 1>&2
      echo
      commands
      echo
      exit 1

  esac

  echo
  echo -e $BOLD"🛑  [$BLUE$1$NOCOLOR] is removed."$NOBOLD

}

IFS=',' read -ra CMD_SPLITS <<< "$CMDS"
for i in "${CMD_SPLITS[@]}"; do
  apply_cmd $i
  echo
done
