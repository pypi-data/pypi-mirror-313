#! /usr/bin/env bash

function abcli_metadata_get() {
    local options=$1
    local source_type=$(abcli_option_choice "$options" object,path,filename object)

    local source=$2
    [[ "$source_type" == object ]] &&
        source=$(abcli_clarify_object $2 .)

    local key=$(abcli_option "$options" key)
    local default=$(abcli_option "$options" default)

    python3 -m blue_objects.metadata get \
        --default "$default" \
        --delim $(abcli_option "$options" delim ,) \
        --dict_keys $(abcli_option_int "$options" dict.keys 0) \
        --dict_values $(abcli_option_int "$options" dict.values 0) \
        --filename $(abcli_option "$options" filename metadata.yaml) \
        --key "$key" \
        --source "$source" \
        --source_type $source_type \
        "${@:3}"
}
