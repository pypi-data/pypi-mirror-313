#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Local Plane"$NOCOLOR$NOBOLD
echo

echo Setting OTEL_SDK_DISABLED
export OTEL_SDK_DISABLED="true"
echo Setting DATALAYER_PUB_SUB_ENGINE
export DATALAYER_PUB_SUB_ENGINE="none"
echo Setting DATALAYER_VAULT_URL
export DATALAYER_VAULT_URL=http://localhost:8200

echo Start the local IAM service.
echo open http://localhost:9700/api/iam/version
echo open http://localhost:9700/api/iam/v1/ping
cd $DATALAYER_SERVICES_HOME/iam && \
  make start &

echo Start the local Spacer service.
echo open http://localhost:9900/api/spacer/version
echo open http://localhost:9900/api/spacer/v1/ping
cd $DATALAYER_SERVICES_HOME/spacer && \
  make start &

echo Start the local Library service.
echo open http://localhost:9800/api/library/version
echo open http://localhost:9800/api/library/v1/ping
cd $DATALAYER_SERVICES_HOME/library && \
  make start &

wait

uname_out="$(uname -s)"

case "${uname_out}" in
    Linux*)     export OS=LINUX;;
    Darwin*)    export OS=MACOS;;
#    CYGWIN*)    OS=CYGWIND;;
#    MINGW*)     OS=MINGW;;
    *)          export OS="UNSUPPORTED:${unameOut}"
esac

function kill_port() {
    case "${OS}" in
        LINUX)     fuser -k $1/tcp;;
        MACOS)     lsof -i TCP:$1 | grep LISTEN | awk '{print $2}' | xargs kill -9;;
        *)         echo "Unsupported operating system ${OS}"
    esac    
}

kill_port 9700
kill_port 9800
kill_port 9900
