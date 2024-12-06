#! /usr/bin/env bash

function abcli_ls() {
    local options=$1
    local on_cloud=$(abcli_option_int "$options" cloud 0)
    local on_local=$(abcli_option_int "$options" local 0)

    [[ "$on_cloud" == 1 ]] ||
        [[ "$on_local" == 1 ]] &&
        local object_name=$(abcli_clarify_object $2 .)

    if [ "$on_cloud" == 1 ]; then
        abcli_eval - \
            aws s3 ls $ABCLI_S3_OBJECT_PREFIX/$object_name/
    elif [ "$on_local" == 1 ]; then
        abcli_eval - \
            ls -1lh $ABCLI_OBJECT_ROOT/$object_name
    else
        abcli_eval - \
            ls -1 "$@"
    fi

    return 0
}
