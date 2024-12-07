#! /usr/bin/env bash

function abcli_mlflow_tags_set() {
    local object_name=$(abcli_clarify_object $1 .)

    local tags=$2

    python3 -m blue_objects.mlflow \
        set_tags \
        --object_name $object_name \
        --tags "$tags" \
        "${@:3}"
}
