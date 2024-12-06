#! /usr/bin/env bash

function abcli_cp() {
    abcli_clone "$@"
}

function abcli_clone() {
    local options=$1
    local clone_tags=$(abcli_option_int "$options" tags 1)
    local do_relate=$(abcli_option_int "$options" relate 1)
    local do_download=$(abcli_option_int "$options" download 1)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local transfer_mechanism=$(abcli_option_choice "$options" cp,mv mv)

    local object_1_name=$(abcli_clarify_object $2 ..)
    local object_2_name=$(abcli_clarify_object $3 .)

    abcli_log "$object_1_name -clone:$transfer_mechanism-> $object_2_name"

    [[ "$do_download" == 1 ]] &&
        abcli_download - $object_1_name

    local object_1_path=$ABCLI_OBJECT_ROOT/$object_1_name
    local object_2_path=$ABCLI_OBJECT_ROOT/$object_2_name

    abcli_eval - \
        rsync \
        -avv \
        $object_1_path/ \
        $object_2_path

    [[ "$clone_tags" == 1 ]] &&
        abcli_tags clone \
            $object_1_name \
            $object_2_name

    [[ "$do_relate" == 1 ]] &&
        abcli_tags set \
            $object_2_name \
            cloned.$object_1_name

    pushd $object_2_path >/dev/null
    local filename
    for filename in $object_1_name.*; do
        $transfer_mechanism -v \
            $filename \
            $object_2_path/$object_2_name.${filename##*.}
    done
    popd >/dev/null

    [[ -f "$object_1_path/metadata.yaml" ]] &&
        cp -v \
            $object_1_path/metadata.yaml \
            $object_2_path/metadata-$object_1_name.yaml

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_2_name

    return 0
}
