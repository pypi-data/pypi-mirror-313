#! /usr/bin/env bash

function abcli_gif() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_clarify_object $2 .)

    [[ "$do_download" == 1 ]] &&
        abcli_download - $object_name

    abcli_log "generating animated gif: $object_name ..."

    abcli_eval dryrun=$do_dryrun \
        python3 -m blue_objects.graphics \
        generate_animated_gif \
        --object_name $object_name \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    return $status
}
