#! /usr/bin/env bash

function abcli_mlflow_test() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_eval dryrun=$do_dryrun \
        python3 -m blue_objects.mlflow \
        test \
        "$@"
}
