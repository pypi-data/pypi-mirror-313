#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Telepresence Install"$NOCOLOR$NOBOLD

# https://www.telepresence.io/docs/latest/quick-start


function install_on_linux() {
    # 1. Download the latest binary (~95 MB):
    sudo curl -fL https://app.getambassador.io/download/tel2oss/releases/download/v2.17.0/telepresence-linux-amd64 -o /usr/local/bin/telepresence
    # 2. Make the binary executable:
    sudo chmod a+x /usr/local/bin/telepresence
}

function install_on_macos() {
    # Intel Macs
    # 1. Download the latest binary (~105 MB):
    sudo curl -fL https://app.getambassador.io/download/tel2oss/releases/download/v2.17.1/telepresence-darwin-amd64 -o /usr/local/bin/telepresence
    # 2. Make the binary executable:
    sudo chmod a+x /usr/local/bin/telepresence
}

case "${OS}" in
    LINUX)     install_on_linux;;
    MACOS)     install_on_macos;;
    *)         echo "Unsupported operating system ${OS}"
esac
