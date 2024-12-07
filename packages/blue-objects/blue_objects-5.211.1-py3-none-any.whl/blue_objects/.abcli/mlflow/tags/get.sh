#! /usr/bin/env bash

function abcli_mlflow_tags_get() {
    local object_name=$(abcli_clarify_object $1 .)

    python3 -m blue_objects.mlflow \
        get_tags \
        --object_name $object_name \
        "${@:2}"
}
