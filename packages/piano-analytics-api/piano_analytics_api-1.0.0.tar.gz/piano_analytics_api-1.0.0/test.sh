#!/bin/bash

function test_version {
    rm -rf env_test
    "python$1" -m venv env_test || return 1
    "env_test/bin/python$1" -m pip install --upgrade pip | grep -v 'already satisfied'
    env_test/bin/pip3 install -r dev-requirements.txt | grep -v 'already satisfied'
    if [[ ! ${PIPESTATUS[0]} -eq 0 ]]; then
        return 1
    fi
    env_test/bin/pytest -vv tests/* || return 1
    rm -rf env_test
}

projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# projectnaam="$(basename "$projectdir")"
cd "$projectdir" || exit 1

./set-env.sh || exit 1
env/bin/pytest -vv tests/* || exit 1

test_version 3.9 || exit 1
test_version 3.11 || exit 1
test_version 3.12 || exit 1
test_version 3.13 || exit 1
