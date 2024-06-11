#!/usr/bin/env bash

if ! command -v pyenv >/dev/null; then
    echo "pyenv is not installed" >&2
    exit 1
fi

if [ -z ${GITHUB_WORKSPACE+x} ]; then
    GITHUB_WORKSPACE="$(dirname $0)/../"
fi

for version in $(cat ".python-version"); do
    case "$version" in
    "3."*)
        export LATEST_PYTHON="$version"
        ;;
    "pypy3."*)
        export LATEST_PYPY="$version"
        ;;
    esac
done

install_latest_python() {
    pyenv install -s "$LATEST_PYTHON" && pyenv install -s "$LATEST_PYPY"
}

function update_pyenv() {
    if command -v brew; then
        brew update
        brew install pyenv
        brew upgrade pyenv
    else
        pushd "$(pyenv root)"
        git pull || true
        popd
    fi
}

create_venv() {
    CURRENT_BASE="$(pyenv virtualenv-prefix "$1" 2>/dev/null || true)"
    if [ ! -z "$CURRENT_BASE" ]; then
        CURRENT_BASE="$(basename $CURRENT_BASE)"
    fi

    if [ "$CURRENT_BASE" != "$2" ]; then
        pyenv virtualenv-delete -f "$1" || true
        pyenv virtualenv -f "$2" "$1"
        PYENV_VERSION="$1" pip install wheel
    else
        echo "$1 is up to date"
    fi
}