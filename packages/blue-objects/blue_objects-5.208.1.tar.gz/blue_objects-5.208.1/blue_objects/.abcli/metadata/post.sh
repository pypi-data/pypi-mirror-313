#! /usr/bin/env bash

function abcli_metadata_post() {
    local key=$1

    local value=$2

    local options=$3
    local source_type=$(abcli_option_choice "$options" object,path,filename object)

    local source=$4
    [[ "$source_type" == object ]] &&
        source=$(abcli_clarify_object $4 .)

    python3 -m blue_objects.metadata post \
        --filename $(abcli_option "$options" filename metadata.yaml) \
        --key "$key" \
        --value "$value" \
        --source "$source" \
        --source_type $source_type \
        "${@:5}"
}
