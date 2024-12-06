#! /usr/bin/env bash

function abcli_mlflow_log_run() {
    local object_name=$(abcli_clarify_object $1 .)

    python3 -m blue_objects.mlflow \
        log_run \
        --object_name $object_name \
        "${@:2}"
}
