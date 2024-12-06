#! /usr/bin/env bash

function abcli_mlflow_tags_clone() {
    local source_object=$(abcli_clarify_object $1 ..)

    local destination_object=$(abcli_clarify_object $2 .)

    abcli_log "mlflow: tags: clone: $source_object -> $destination_object ..."

    python3 -m blue_objects.mlflow \
        clone_tags \
        --destination_object $destination_object \
        --source_object $source_object \
        "${@:3}"
}
