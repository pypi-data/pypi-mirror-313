#! /usr/bin/env bash

function abcli_mlflow_tags_search() {
    local options=$1
    local is_explicit=$(abcli_option_int "$options" explicit 0)

    python3 -m blue_objects.mlflow \
        search \
        --explicit_query $is_explicit \
        --tags "$options" \
        "${@:2}"
}
