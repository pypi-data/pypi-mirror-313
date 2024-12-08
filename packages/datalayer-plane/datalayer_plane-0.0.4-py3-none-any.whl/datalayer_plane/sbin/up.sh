#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Deploying Datalayer Plane"$NOCOLOR$NOBOLD
echo

function kubernetes_telepresence() {
  export RELEASE=kubernetes-telepresence
  export NAMESPACE=ambassador
  helm upgrade \
    --install $RELEASE \
    datawire/telepresence \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/kubernetes-telepresence/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
}

function kubernetes_dashboard() {
  export RELEASE=kubernetes-dashboard
  export NAMESPACE=kube-system
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/kubernetes-dashboard \
    --create-namespace \
    --namespace $NAMESPACE \
    --timeout 5m
}

function datalayer_nginx() {
  export RELEASE=datalayer-nginx
  export NAMESPACE=datalayer-nginx
  helm upgrade \
    --install $RELEASE \
    ingress-nginx/ingress-nginx \
    --version 4.10.1 \
    --namespace $NAMESPACE \
    --create-namespace \
    --values $PLANE_HOME/etc/helm/charts/datalayer-nginx/values-any.yaml \
    --set controller.image.registry="${DATALAYER_DOCKER_REGISTRY}" \
    --timeout 5m
#  helm upgrade \
#    --install $RELEASE \
#    $PLANE_HOME/etc/helm/charts/datalayer-nginx \
#    --create-namespace \
#    --namespace $NAMESPACE \
#    --values $PLANE_HOME/etc/helm/charts/datalayer-nginx/values-$DATALAYER_CLUSTER_TYPE.yaml \
#    --set router.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
#    --set router.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
#    --set router.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
#    --set router.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
#    --set router.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
#    --set router.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
#    --set router.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
#    --set router.env.DATALAYER_LDAP_BIND="${DATALAYER_LDAP_BIND}" \
#    --set router.env.DATALAYER_LDAP_BIND_PWD="${DATALAYER_LDAP_BIND_PWD}" \
#    --set router.env.DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET="${DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET}" \
#    --timeout 5m
}

function datalayer_traefik() {
  export RELEASE=datalayer-traefik
  export NAMESPACE=datalayer-traefik
  helm upgrade \
    --install $RELEASE \
    traefik/traefik \
    --version 28.0.0 \
    --namespace $NAMESPACE \
    --create-namespace \
    --values $PLANE_HOME/etc/helm/charts/datalayer-traefik/values-any.yaml \
    --timeout 5m
}

function datalayer_cert_manager() {
  export RELEASE=datalayer-cert-manager
  export NAMESPACE=datalayer-cert-manager
  helm upgrade \
    --install $RELEASE \
    jetstack/cert-manager \
    --version v1.13.4 \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-cert-manager/values-any.yaml \
    --timeout 5m
}

function datalayer_cuda_operator() {
  export RELEASE=datalayer-cuda-operator
  export NAMESPACE=datalayer-cuda-operator

  # use 'none' for time slicing, otherwise use 'single' (or 'mixed').
  export MIG_STRATEGY="none"

  echo
  echo -e $YELLOW"Creating the gpu-cuda-timeslicing-config-all Configmap..."$NOCOLOR
  echo
# replicas: 20
# migStrategy: single | none | mixed
  cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: gpu-cuda-timeslicing-config-all
  namespace: datalayer-cuda-operator
data:
  gpu-cuda-timeslicing-default: |-
    version: v1
    flags:
      migStrategy: ${MIG_STRATEGY}
    sharing:
      timeSlicing:
        renameByDefault: false
        failRequestsGreaterThanOne: false
        resources:
        - name: nvidia.com/gpu
          replicas: 2
EOF

  # For time-slicing.
  # --set mig.strategy=none \
  # --set devicePlugin.config.name="gpu-cuda-timeslicing-config-all" \

  # MIG options.
  # --set migManager.enabled=false \
  # --set mig.strategy=none | single | mixed \

  # Toolkit and Driver.
  # --set toolkit.enabled=true \
  # --set driver.enabled=false \

  echo
  echo -e $YELLOW"Installing the nvidia/gpu-operator Helm chart..."$NOCOLOR
  echo
  helm upgrade \
    --install $RELEASE \
    nvidia/gpu-operator \
    --create-namespace \
    --namespace $NAMESPACE \
    --set devicePlugin.config.name=gpu-cuda-timeslicing-config-all \
    --set mig.strategy=${MIG_STRATEGY} \
    --values $PLANE_HOME/etc/helm/charts/datalayer-cuda-operator/values-any.yaml \
    --timeout 5m

  echo
  echo -e $YELLOW"Patching clusterpolicies.nvidia.com/cluster-policy..."$NOCOLOR
  echo
  kubectl patch \
    clusterpolicies.nvidia.com/cluster-policy \
    --namespace datalayer-cuda-operator \
    --type merge \
    --patch='{"spec": {"devicePlugin": {"config": {"name": "gpu-cuda-timeslicing-config-all", "default": "gpu-cuda-timeslicing-default"}}}}'

  echo
  echo -e $YELLOW"Labelling Nodes for device plugin config..."$NOCOLOR
  echo
  kubectl label --overwrite node nvidia.com/device-plugin.config=gpu-cuda-timeslicing-default -l xpu.datalayer.io/gpu-cuda=true

}

function datalayer_datashim() {
  if [ -z "$(helm repo list | grep datashim)" ]; then
    helm repo add datashim https://datashim-io.github.io/datashim/
    helm repo update datashim
  fi
  export RELEASE=datalayer-datashim
  export NAMESPACE=datalayer-datashim
  helm upgrade \
    --install $RELEASE \
    datashim/datashim-charts \
    --create-namespace \
    --namespace=$NAMESPACE \
    --version 0.4.0 \
    --values $PLANE_HOME/etc/helm/charts/datalayer-datashim/values-any.yaml \
    --timeout 5m
}

function datalayer_solr_operator() {
  if [ -z "$(helm repo list | grep apache-solr)" ]; then
    helm repo add apache-solr https://solr.apache.org/charts
    helm repo update apache-solr
  fi
  export RELEASE=datalayer-solr-operator
  export NAMESPACE=datalayer-solr-operator
  kubectl create \
    -n $NAMESPACE \
    -f https://solr.apache.org/operator/downloads/crds/v0.8.1/all-with-dependencies.yaml
  helm upgrade \
    --install $RELEASE \
    apache-solr/solr-operator \
    --version 0.8.1 \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-solr-operator/values-any.yaml \
    --timeout 5m
}

function etcd() {
  helm install \
    etcd \
    --set StorageClass=gp2 \
    -n etcd
}

function hdfs() {
  helm install \
    hdfs \
    --set imagePullPolicy=Always \
    --set persistence.nameNode.enabled=true \
    --set persistence.nameNode.storageClass=gp2 \
    --set persistence.dataNode.enabled=true \
    --set persistence.dataNode.storageClass=gp2 \
    --set hdfs.dataNode.replicas=3 \
    -n hdfs
}

function spark() {
  helm install \
    spark \
    --set spark.imagePullPolicy=Always \
    -n spark
}

function jupyterpool() {
  export RELEASE=jupyterpool
  export NAMESPACE=datalayer
#    --set jupyterpool.env.GITHUB_CLIENT_ID=${DATALAYER_GITHUB_OAUTH_CLIENT_ID} \
#    --set jupyterpool.env.GITHUB_CLIENT_SECRET=${DATALAYER_GITHUB_OAUTH_CLIENT_SECRET} \
#    --set jupyterpool.env.GITHUB_OAUTH_CALLBACK_URL=${DATALAYER_GITHUB_OAUTH_CALLBACK_URL} \
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/jupyterpool \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/jupyterpool/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set jupyterpool.env.DATALAYER_RUN_URL=${DATALAYER_RUN_URL} \
    --timeout 5m
}

function jupyter_server() {
  export RELEASE=jupyter-server
  export NAMESPACE=datalayer-api
#    --set server.env.GITHUB_CLIENT_ID=${DATALAYER_GITHUB_OAUTH_CLIENT_ID} \
#    --set server.env.GITHUB_CLIENT_SECRET=${DATALAYER_GITHUB_OAUTH_CLIENT_SECRET} \
#    --set server.env.GITHUB_OAUTH_CALLBACK_URL=${DATALAYER_GITHUB_OAUTH_CALLBACK_URL} \
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/jupyter-server \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/jupyter-server/values-any.yaml \
    --set server.image="${DATALAYER_DOCKER_REGISTRY}/jupyter-server:0.0.9" \
    --set server.env.DATALAYER_RUN_URL=${DATALAYER_RUN_URL} \
    --timeout 5m
}

#    --set jupyter-editor.env.GITHUB_CLIENT_ID=${DATALAYER_GITHUB_OAUTH_CLIENT_ID} \
#    --set jupyter-editor.env.GITHUB_CLIENT_SECRET=${DATALAYER_GITHUB_OAUTH_CLIENT_SECRET} \
#    --set jupyter-editor.env.GITHUB_OAUTH_CALLBACK_URL=${DATALAYER_GITHUB_OAUTH_CALLBACK_URL} \
function jupyter_editor() {
  export RELEASE=jupyter-editor
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/jupyter-editor \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/jupyter-editor/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set jupyter-editor.env.DATALAYER_RUN_URL=${DATALAYER_RUN_URL} \
    --timeout 5m
}

#    --set jupyterhub.singleuser.extraEnv.DATALAYER_GITHUB_TOKEN=${DATALAYER_GITHUB_TOKEN} \
#    --set jupyterhub.singleuser.extraEnv.DATALAYER_TWITTER_OAUTH_CONSUMER_KEY=${DATALAYER_TWITTER_OAUTH_CONSUMER_KEY} \
#    --set jupyterhub.singleuser.extraEnv.DATALAYER_TWITTER_OAUTH_CONSUMER_SECRET=${DATALAYER_TWITTER_OAUTH_CONSUMER_SECRET} \
function jupyterhub() {
  export RELEASE=jupyterhub
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/jupyterhub \
    --create-namespace \
    --version 0.11.1 \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/jupyterhub/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set jupyterhub.proxy.secretToken=${DATALAYER_JUPYTERHUB_HTTP_PROXY_AUTH_TOKEN} \
    --set jupyterhub.hub.db.password=${DATALAYER_JUPYTERHUB_DB_PWD} \
    --set jupyterhub.hub.extraEnv.JUPYTERHUB_CRYPT_KEY=${JUPYTERHUB_CRYPT_KEY} \
    --set jupyterhub.hub.extraEnv.DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET=${DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET} \
    --set jupyterhub.hub.extraEnv.DATALAYER_TWITTER_OAUTH_CONSUMER_KEY=${DATALAYER_TWITTER_OAUTH_CONSUMER_KEY} \
    --set jupyterhub.hub.extraEnv.DATALAYER_TWITTER_OAUTH_CONSUMER_SECRET=${DATALAYER_TWITTER_OAUTH_CONSUMER_SECRET} \
    --timeout 5m
}

function datalayer_ceph_operator() {
  export RELEASE=datalayer-ceph-operator
  export NAMESPACE=datalayer-storage
  if [ -z "$(helm repo list | grep rook-release)" ]; then
    helm repo add rook-release https://charts.rook.io/release
    helm repo update rook-release
  fi
  helm upgrade \
    --install $RELEASE \
    rook-release/rook-ceph \
    --version 1.15.1 \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-ceph-operator/values.yaml \
    --timeout 10m
}

function datalayer_ceph_cluster() {
  export RELEASE=datalayer-ceph-cluster
  export NAMESPACE=datalayer-storage
  if [ -z "$(helm repo list | grep rook-release)" ]; then
    helm repo add rook-release https://charts.rook.io/release
    helm repo update rook-release
  fi
  helm upgrade \
    --install $RELEASE \
    rook-release/rook-ceph-cluster \
    --version 1.15.1 \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-ceph-cluster/values.yaml \
    --set clusterName=${DATALAYER_RUN_URL} \
    --timeout 10m
}

function datalayer_shared_filesystem() {
  export RELEASE=datalayer-shared-filesystem
  export NAMESPACE=datalayer-storage
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-shared-filesystem \
    --create-namespace \
    --namespace $NAMESPACE \
    --set sharedStorage.sharedFsPVC="${DATALAYER_USERS_PVC_NAME}" \
    --set sharedStorage.storageProvider="${DATALAYER_STORAGE_PROVIDER}"
}

function datalayer_config() {
  export RELEASE=datalayer-config
  export NAMESPACE=datalayer-config
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-config \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-config/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
}

function datalayer_mailer() {
  export RELEASE=datalayer-mailer
  export NAMESPACE=datalayer-system
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-mailer \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-mailer/values.yaml \
    --set mailer.image="${DATALAYER_DOCKER_REGISTRY}/mailer:0.0.1" \
    --set mailer.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set mailer.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set mailer.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set mailer.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --timeout 5m
}

function datalayer_vault() {
  export RELEASE=datalayer-vault
  export NAMESPACE=datalayer-vault
  helm upgrade \
    --install $RELEASE \
    hashicorp/vault \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-vault/values-any.yaml \
    --timeout 5m
}

function datalayer_pulsar() {
  export RELEASE=datalayer-pulsar
  export NAMESPACE=datalayer-pulsar
  if [ -z "$(helm repo list | grep pulsar)" ]; then
    helm repo add apache https://pulsar.apache.org/charts
    helm repo update apache
  fi
  helm upgrade \
    --install $RELEASE \
    apache/pulsar \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-pulsar/values-any.yaml \
    --timeout 10m
}

function datalayer_ldap() {
  export RELEASE=datalayer-ldap
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/ldap \
    --create-namespace \
    --namespace $NAMESPACE \
    --timeout 5m \
    --values $PLANE_HOME/etc/helm/charts/ldap/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set adminPassword=${DATALAYER_LDAP_BIND_PWD} \
    --set configPassword=${DATALAYER_LDAP_BIND_PWD}
}

function datalayer_ldapadmin() {
  export RELEASE=datalayer-ldap
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/ldapadmin \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/ldapadmin/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
}

function datalayer_keycloak() {
  export RELEASE=datalayer-keycloak
  export NAMESPACE=datalayer
#    $PLANE_HOME/etc/helm/charts/keycloak \
#    --set postgresql.postgresqlPassword=${DATALAYER_KEYCLOAK_DB_PWD} \
#    --set persistence.dbPassword=${DATALAYER_KEYCLOAK_DB_PWD} \
#    --set dbPassword=${DATALAYER_KEYCLOAK_DB_PWD} \
  helm upgrade \
    --install $RELEASE \
    codecentric/keycloak \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/keycloak/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set keycloak.password=${DATALAYER_KEYCLOAK_PWD} \
    --timeout 5m
}

#    --set accessKey=${DATALAYER_MINIO_ACCESS_KEY} \
#    --set secretKey=${DATALAYER_MINIO_SECRET_KEY} \
#    --set minio.DATALAYER_MINIO_TENANT_URL=${DATALAYER_AUTH_AUTH_CALLBACK} \
function datalayer_minio() {
  export RELEASE=datalayer-minio
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/minio \
    --create-namespace \
    --namespace datalayer-minio \
    --values $PLANE_HOME/etc/helm/charts/minio/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
  kubectl apply -f $PLANE_HOME/etc/helm/charts/minio/specs/tenant.yaml
  kubectl minio init
  kubectl create namespace $NAMESPACE
}

function datalayer_observer() {
  export RELEASE=datalayer-observer
  export NAMESPACE=datalayer-observer
  # Build dependency if needed
  if [ ! -f "${PLANE_HOME}/etc/helm/charts/datalayer-observer/requirements.lock" ]; then
    helm dependency build $PLANE_HOME/etc/helm/charts/datalayer-observer
  fi
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-observer \
    --create-namespace \
    --namespace $NAMESPACE \
    --set observer.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set kube-prometheus-stack.grafana."grafana\.ini".server.domain="${DATALAYER_RUN_URL}" \
    --set kube-prometheus-stack.grafana."grafana\.ini".server.root_url=https://"${DATALAYER_RUN_URL}"/grafana \
    --set kube-prometheus-stack.grafana.adminPassword="${DATALAYER_GRAFANA_ADMIN_PASSWORD}" \
    --timeout 5m
}

function datalayer_iam() {
  export RELEASE=datalayer-iam
  export NAMESPACE=datalayer-api
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-iam \
    --create-namespace \
    --namespace $NAMESPACE \
    --set iam.image="${DATALAYER_DOCKER_REGISTRY}/iam:1.0.4" \
    --set iam.certificateIssuer="letsencrypt" \
    --set iam.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set iam.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
    --set iam.env.DATALAYER_CREDITS_PROVIDER="${DATALAYER_CREDITS_PROVIDER}" \
    --set iam.env.DATALAYER_GITHUB_CLIENT_ID="${DATALAYER_GITHUB_CLIENT_ID}" \
    --set iam.env.DATALAYER_GITHUB_CLIENT_SECRET="${DATALAYER_GITHUB_CLIENT_SECRET}" \
    --set iam.env.DATALAYER_IAM_API_KEY="${DATALAYER_IAM_API_KEY}" \
    --set iam.env.DATALAYER_JWT_ALGORITHM="${DATALAYER_JWT_ALGORITHM}" \
    --set iam.env.DATALAYER_JWT_ALLOWED_ISSUERS="${DATALAYER_JWT_ALLOWED_ISSUERS}" \
    --set iam.env.DATALAYER_JWT_CACHE_VALIDATE="${DATALAYER_JWT_CACHE_VALIDATE}" \
    --set iam.env.DATALAYER_JWT_DEFAULT_KID_ISSUER="${DATALAYER_JWT_DEFAULT_KID_ISSUER}" \
    --set iam.env.DATALAYER_JWT_ISSUER="${DATALAYER_JWT_ISSUER}" \
    --set iam.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set iam.env.DATALAYER_JWT_SKIP_EXTERNAL_TOKEN_SIGNATURE_VERIFICATION="${DATALAYER_JWT_SKIP_EXTERNAL_TOKEN_SIGNATURE_VERIFICATION}" \
    --set iam.env.DATALAYER_LINKEDIN_CLIENT_ID="${DATALAYER_LINKEDIN_CLIENT_ID}" \
    --set iam.env.DATALAYER_LINKEDIN_CLIENT_SECRET="${DATALAYER_LINKEDIN_CLIENT_SECRET}" \
    --set iam.env.DATALAYER_OPENFGA_AUTHZ_MODEL_ID="${DATALAYER_OPENFGA_AUTHZ_MODEL_ID}" \
    --set iam.env.DATALAYER_OPENFGA_REST_URL="${DATALAYER_OPENFGA_REST_URL}" \
    --set iam.env.DATALAYER_OPENFGA_STORE_ID="${DATALAYER_OPENFGA_STORE_ID}" \
    --set iam.env.DATALAYER_PUB_SUB_ENGINE="${DATALAYER_PUB_SUB_ENGINE}" \
    --set iam.env.DATALAYER_PULSAR_URL="${DATALAYER_PULSAR_URL}" \
    --set iam.env.DATALAYER_RUNTIME_ENV="${DATALAYER_RUNTIME_ENV}" \
    --set iam.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set iam.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set iam.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set iam.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set iam.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --set iam.env.DATALAYER_STRIPE_API_KEY="${DATALAYER_STRIPE_API_KEY}" \
    --set iam.env.DATALAYER_STRIPE_CHECKOUT_ROUTE="${DATALAYER_STRIPE_CHECKOUT_ROUTE}" \
    --set iam.env.DATALAYER_STRIPE_JS_API_KEY="${DATALAYER_STRIPE_JS_API_KEY}" \
    --set iam.env.DATALAYER_STRIPE_PRODUCT_ID="${DATALAYER_STRIPE_PRODUCT_ID}" \
    --set iam.env.DATALAYER_STRIPE_WEBHOOK_SECRET="${DATALAYER_STRIPE_WEBHOOK_SECRET}" \
    --set iam.env.DATALAYER_SUPPORT_EMAIL="${DATALAYER_SUPPORT_EMAIL}" \
    --set iam.env.DATALAYER_VAULT_TOKEN="${DATALAYER_VAULT_TOKEN}" \
    --set iam.env.DATALAYER_VAULT_URL="${DATALAYER_VAULT_URL}" \
    --set iam.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set iam.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set iam.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
    --timeout 5m
}

function datalayer_jupyter() {
  export RELEASE=datalayer-jupyter
  export NAMESPACE=datalayer-api
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-jupyter \
    --create-namespace \
    --namespace $NAMESPACE \
    --set jupyter.image="${DATALAYER_DOCKER_REGISTRY}/jupyter:1.0.3" \
    --set jupyter.certificateIssuer="letsencrypt" \
    --set jupyter.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set jupyter.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
    --set jupyter.env.DATALAYER_JWT_ALGORITHM="${DATALAYER_JWT_ALGORITHM}" \
    --set jupyter.env.DATALAYER_JWT_CACHE_VALIDATE="${DATALAYER_JWT_CACHE_VALIDATE}" \
    --set jupyter.env.DATALAYER_JWT_ISSUER="${DATALAYER_JWT_ISSUER}" \
    --set jupyter.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set jupyter.env.DATALAYER_OPENFGA_AUTHZ_MODEL_ID="${DATALAYER_OPENFGA_AUTHZ_MODEL_ID}" \
    --set jupyter.env.DATALAYER_OPENFGA_REST_URL="${DATALAYER_OPENFGA_REST_URL}" \
    --set jupyter.env.DATALAYER_OPENFGA_STORE_ID="${DATALAYER_OPENFGA_STORE_ID}" \
    --set jupyter.env.DATALAYER_OPERATOR_API_KEY="${DATALAYER_OPERATOR_API_KEY}" \
    --set jupyter.env.DATALAYER_PUB_SUB_ENGINE="${DATALAYER_PUB_SUB_ENGINE}" \
    --set jupyter.env.DATALAYER_PULSAR_URL="${DATALAYER_PULSAR_URL}" \
    --set jupyter.env.DATALAYER_RUNTIME_ENV="${DATALAYER_RUNTIME_ENV}" \
    --set jupyter.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set jupyter.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set jupyter.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set jupyter.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
    --timeout 5m
}

function datalayer_operator() {
  export RELEASE=datalayer-operator
  export NAMESPACE=datalayer-jupyter
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-operator \
    --create-namespace \
    --namespace $NAMESPACE \
    --set operator.image="${DATALAYER_DOCKER_REGISTRY}/operator:1.0.7" \
    --set operator.crds="true" \
    --set operator.sharedFsPVC="${DATALAYER_USERS_PVC_NAME}" \
    --set operator.env.AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    --set operator.env.AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    --set operator.env.AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    --set operator.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set operator.env.DATALAYER_CERT_ISSUER="${DATALAYER_CERT_ISSUER}" \
    --set operator.env.DATALAYER_DOCKER_REGISTRY="${DATALAYER_DOCKER_REGISTRY}" \
    --set operator.env.DATALAYER_IAM_API_KEY="${DATALAYER_IAM_API_KEY}" \
    --set operator.env.DATALAYER_IAM_HOST="${DATALAYER_IAM_HOST}" \
    --set operator.env.DATALAYER_INGRESS_CLASS_NAME="${DATALAYER_INGRESS_CLASS_NAME}" \
    --set operator.env.DATALAYER_OPERATOR_API_KEY="${DATALAYER_OPERATOR_API_KEY}" \
    --set operator.env.DATALAYER_PUB_SUB_ENGINE="${DATALAYER_PUB_SUB_ENGINE}" \
    --set operator.env.DATALAYER_PULSAR_URL="${DATALAYER_PULSAR_URL}" \
    --set operator.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set operator.env.DATALAYER_VAULT_TOKEN="${DATALAYER_VAULT_TOKEN}" \
    --set operator.env.DATALAYER_VAULT_URL="${DATALAYER_VAULT_URL}" \
    --set operator.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set operator.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set operator.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
   --timeout 5m
}

#    --set nodeSelector."role\\.datalayer\\.io/system="\"true\""" \
function datalayer_openfga() {
  export RELEASE=datalayer-openfga
  export NAMESPACE=datalayer-openfga
  helm upgrade \
    --install $RELEASE \
    openfga/openfga \
    --values $PLANE_HOME/etc/helm/charts/datalayer-openfga/values-any.yaml \
    --set datastore.engine=postgres \
    --set datastore.uri="postgres://postgres:password@$NAMESPACE-postgresql-hl.$NAMESPACE.svc.cluster.local:5432/postgres?sslmode=disable" \
    --set postgresql.enabled=true \
    --set postgresql.auth.database=postgres \
    --set postgresql.auth.postgresPassword=password \
    --create-namespace \
    --namespace $NAMESPACE \
    --timeout 5m
}

function datalayer_spacer() {
  export RELEASE=datalayer-spacer
  export NAMESPACE=datalayer-api
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-spacer \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-spacer/values-any.yaml \
    --set spacer.image="${DATALAYER_DOCKER_REGISTRY}/spacer:0.0.6" \
    --set spacer.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set spacer.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
    --set spacer.env.DATALAYER_RUNTIME_ENV="${DATALAYER_RUNTIME_ENV}" \
    --set spacer.env.AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    --set spacer.env.AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    --set spacer.env.AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    --set spacer.env.DATALAYER_JWT_ISSUER="${DATALAYER_JWT_ISSUER}" \
    --set spacer.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set spacer.env.DATALAYER_JWT_ALGORITHM="${DATALAYER_JWT_ALGORITHM}" \
    --set spacer.env.DATALAYER_JWT_CACHE_VALIDATE="${DATALAYER_JWT_CACHE_VALIDATE}" \
    --set spacer.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set spacer.env.DATALAYER_OPENFGA_REST_URL="${DATALAYER_OPENFGA_REST_URL}" \
    --set spacer.env.DATALAYER_OPENFGA_STORE_ID="${DATALAYER_OPENFGA_STORE_ID}" \
    --set spacer.env.DATALAYER_OPENFGA_AUTHZ_MODEL_ID="${DATALAYER_OPENFGA_AUTHZ_MODEL_ID}" \
    --set spacer.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set spacer.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set spacer.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --set spacer.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set spacer.env.DATALAYER_SOLR_USERNAME="${DATALAYER_SOLR_USERNAME}" \
    --set spacer.env.DATALAYER_SOLR_PASSWORD="${DATALAYER_SOLR_PASSWORD}" \
    --set spacer.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set spacer.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set spacer.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
    --timeout 5m
}

function datalayer_library() {
  export RELEASE=datalayer-library
  export NAMESPACE=datalayer-api
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-library \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-library/values-any.yaml \
    --set library.image="${DATALAYER_DOCKER_REGISTRY}/library:0.0.6" \
    --set library.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set library.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
    --set library.env.DATALAYER_RUNTIME_ENV="${DATALAYER_RUNTIME_ENV}" \
    --set library.env.AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    --set library.env.AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    --set library.env.AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    --set library.env.DATALAYER_JWT_ISSUER="${DATALAYER_JWT_ISSUER}" \
    --set library.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set library.env.DATALAYER_JWT_ALGORITHM="${DATALAYER_JWT_ALGORITHM}" \
    --set library.env.DATALAYER_JWT_CACHE_VALIDATE="${DATALAYER_JWT_CACHE_VALIDATE}" \
    --set library.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set library.env.DATALAYER_OPENFGA_REST_URL="${DATALAYER_OPENFGA_REST_URL}" \
    --set library.env.DATALAYER_OPENFGA_STORE_ID="${DATALAYER_OPENFGA_STORE_ID}" \
    --set library.env.DATALAYER_OPENFGA_AUTHZ_MODEL_ID="${DATALAYER_OPENFGA_AUTHZ_MODEL_ID}" \
    --set library.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set library.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set library.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --set library.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set library.env.DATALAYER_SOLR_USERNAME="${DATALAYER_SOLR_USERNAME}" \
    --set library.env.DATALAYER_SOLR_PASSWORD="${DATALAYER_SOLR_PASSWORD}" \
    --set library.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set library.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set library.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
    --timeout 5m
}

function datalayer_manager() {
  export RELEASE=datalayer-manager
  export NAMESPACE=datalayer-api
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-manager \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-manager/values-any.yaml \
    --set manager.image="${DATALAYER_DOCKER_REGISTRY}/manager:0.0.1" \
    --set manager.ingress="true" \
    --set manager.env.DATALAYER_RUN_URL="${DATALAYER_RUN_URL}" \
    --set manager.env.DATALAYER_CDN_URL="${DATALAYER_CDN_URL}" \
    --set manager.env.DATALAYER_RUNTIME_ENV="${DATALAYER_RUNTIME_ENV}" \
    --set manager.env.AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    --set manager.env.AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    --set manager.env.AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    --set manager.env.DATALAYER_JWT_ISSUER="${DATALAYER_JWT_ISSUER}" \
    --set manager.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set manager.env.DATALAYER_JWT_ALGORITHM="${DATALAYER_JWT_ALGORITHM}" \
    --set manager.env.DATALAYER_JWT_CACHE_VALIDATE="${DATALAYER_JWT_CACHE_VALIDATE}" \
    --set manager.env.DATALAYER_AUTHZ_ENGINE="${DATALAYER_AUTHZ_ENGINE}" \
    --set manager.env.DATALAYER_OPENFGA_REST_URL="${DATALAYER_OPENFGA_REST_URL}" \
    --set manager.env.DATALAYER_OPENFGA_STORE_ID="${DATALAYER_OPENFGA_STORE_ID}" \
    --set manager.env.DATALAYER_OPENFGA_AUTHZ_MODEL_ID="${DATALAYER_OPENFGA_AUTHZ_MODEL_ID}" \
    --set manager.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set manager.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set manager.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --set manager.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set manager.env.DATALAYER_SOLR_USERNAME="${DATALAYER_SOLR_USERNAME}" \
    --set manager.env.DATALAYER_SOLR_PASSWORD="${DATALAYER_SOLR_PASSWORD}" \
    --set manager.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT}" \
    --set manager.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}" \
    --set manager.env.OTEL_PYTHON_LOG_LEVEL="${OTEL_PYTHON_LOG_LEVEL:-info}" \
    --timeout 5m
}

function datalayer_jump() {
  export RELEASE=datalayer-jump
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-jump \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-jump/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
  cat <<EOF >>/tmp/ingress-values.yaml
  tcp:
    22: datalayer/datalayer-jump-svc:2022
EOF
  helm upgrade \
    --install ingress-nginx \
    ingress-nginx/ingress-nginx \
    -n ingress-nginx \
    --values /tmp/ingress-values.yaml
}

function datalayer_content() {
  export RELEASE=datalayer-content
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/datalayer-content \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/datalayer-content/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --timeout 5m
}

function datalayer_editor() {
  export RELEASE=datalayer-editor
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/editor \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/editor/values-$DATALAYER_CLUSTER_TYPE.yaml \
    --set editor.env.DATALAYER_JWT_SECRET="${DATALAYER_JWT_SECRET}" \
    --set editor.env.DATALAYER_SMTP_HOST="${DATALAYER_SMTP_HOST}" \
    --set editor.env.DATALAYER_SMTP_PORT="${DATALAYER_SMTP_PORT}" \
    --set editor.env.DATALAYER_SMTP_USERNAME="${DATALAYER_SMTP_USERNAME}" \
    --set editor.env.DATALAYER_SMTP_PASSWORD="${DATALAYER_SMTP_PASSWORD}" \
    --set editor.env.DATALAYER_LDAP_BIND="${DATALAYER_LDAP_BIND}" \
    --set editor.env.DATALAYER_LDAP_BIND_PWD="${DATALAYER_LDAP_BIND_PWD}" \
    --set editor.env.DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET="${DATALAYER_KEYCLOAK_REALM_CLIENT_SECRET}" \
    --timeout 5m
}

function example_simple() {
  export RELEASE=example-simple
  export NAMESPACE=datalayer
  helm upgrade \
    --install $RELEASE \
    $PLANE_HOME/etc/helm/charts/example-simple \
    --create-namespace \
    --namespace $NAMESPACE \
    --values $PLANE_HOME/etc/helm/charts/example-simple/values-any.yaml \
    --set secret.DATALAYER_LDAP_BIND_PWD=${DATALAYER_LDAP_BIND_PWD} \
    --timeout 5m
}

function commands() {
  echo -e $YELLOW"💛  Valid commands: [ kubernetes-dashboard | datalayer-config | datalayer-operator | datalayer-manager | datalayer-openfga | datalayer-ceph-operator | datalayer-ceph-cluster | datalayer-shared-filesystem | datalayer-vault | datalayer-mailer | datalayer-pulsar | datalayer-cert-manager | datalayer-ldap | datalayer-ldapadmin | datalayer-keycloak | datalayer-iam | datalayer-observer | datalayer-nginx | datalayer-traefik | datalayer-jump | datalayer-content | datalayer-operator | datalayer-spacer | datalayer-library | datalayer-cuda-operator | datalayer-datashim | datalayer-solr-operator | jupyterhub | jupyterpool |  jupyter-server | datalayer-minio | example-simple ]"$NOCOLOR 1>&2
}

CMDS="$1"

if [ -z "$CMDS" ]; then
  echo -e $RED$BOLD"💔  No command to execute has been provided."$NOCOLOR$NOBOLD 1>&2
  echo
  exit 1
fi

# TODO see https://stackoverflow.com/questions/33387263/invoke-function-whose-name-is-stored-in-a-variable-in-bash
# TODO see https://stackoverflow.com/questions/17529220/why-should-eval-be-avoided-in-bash-and-what-should-i-use-instead/17529221#17529221
function apply_cmd() {

  echo -e $BOLD"🔥  Deploying [$BLUE$1$NOCOLOR]"$NOBOLD
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

    datalayer-cuda-operator)
      datalayer_cuda_operator
      ;;

    datalayer-datashim)
      datalayer_datashim
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

    datalayer-mailer)
      datalayer_mailer
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

    datalayer-openfga)
      datalayer_openfga
      ;;

    datalayer-operator)
      datalayer_operator
      ;;

    datalayer-spacer)
      datalayer_spacer
      ;;

    datalayer-library)
      datalayer_library
      ;;

    datalayer-jump)
      datalayer_jump
      ;;

    datalayer-jupyter)
      datalayer_jupyter
      ;;

    datalayer-content)
      datalayer_content
      ;;

    jupyterhub)
      jupyterhub
      ;;

    datalayer-minio)
      datalayer_minio
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
  echo -e $BOLD"✅ [$BLUE$1$NOCOLOR] is deployed."$NOBOLD
  echo

}

IFS=',' read -ra CMD_SPLITS <<< "$CMDS"
for i in "${CMD_SPLITS[@]}"; do
  apply_cmd $i
done
