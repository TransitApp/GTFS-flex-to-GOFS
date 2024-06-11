#!/bin/bash
set -xeu pipefail

. "create_venv.sh"

if [ -z ${GITHUB_ACTIONS+x} ]; then
    SUDO="echo"
else
    SUDO="sudo"
fi

if command -v pyenv >/dev/null; then
    pushd "$(dirname $0)/../"
    install_latest_python || (update_pyenv && install_latest_python)

    git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv || true

    create_venv GTFS-flex-to-GOFS-lite "$LATEST_PYTHON"
else
    echo "Please install pyenv. This script cannot install it for you."
    exit 1
fi