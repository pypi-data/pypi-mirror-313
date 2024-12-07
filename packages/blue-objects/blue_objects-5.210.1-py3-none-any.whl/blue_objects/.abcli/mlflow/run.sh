#! /usr/bin/env bash

function abcli_mlflow_run() {
    local object_name=$(abcli_clarify_object $1 .)

    python3 -m blue_objects.mlflow \
        start_end_run \
        --object_name $object_name \
        --start_end "$2" \
        "${@:3}"
}
