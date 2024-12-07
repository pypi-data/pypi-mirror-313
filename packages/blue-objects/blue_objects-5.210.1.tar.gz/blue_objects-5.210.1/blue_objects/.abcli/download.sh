#! /usr/bin/env bash

function abcli_download() {
    local options=$1
    local filename=$(abcli_option "$options" filename)

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    local open_options=$3

    if [ -f "../$object_name.tar.gz" ]; then
        abcli_log "✅ $object_name.tar.gz already exists - skipping download."
        return 1
    fi

    if [ ! -z "$filename" ]; then
        abcli_log "downloading $object_name/$filename ..."
        aws s3 cp "$ABCLI_S3_OBJECT_PREFIX/$object_name/$filename" "$object_path/$filename"
    else
        local exists=$(aws s3 ls $ABCLI_AWS_S3_BUCKET_NAME/$ABCLI_AWS_S3_PREFIX/$object_name.tar.gz)
        if [ -z "$exists" ]; then
            abcli_log "downloading $object_name ..."

            aws s3 sync \
                "$ABCLI_S3_OBJECT_PREFIX/$object_name" \
                "$object_path" \
                --exact-timestamps
        else
            abcli_log "downloading $object_name.tar.gz ..."

            pushd $ABCLI_OBJECT_ROOT >/dev/null

            aws s3 cp \
                "$ABCLI_S3_OBJECT_PREFIX/$object_name.tar.gz" .

            local object_size=$(blue_objects_file size $object_name.tar.gz)
            abcli_log "$object_name.tar.gz ($object_size) downloaded."

            tar -xvf "$object_name.tar.gz"

            popd >/dev/null
        fi

    fi

    local do_open=$(abcli_option_int "$open_options" open 0)
    [[ "$do_open" == 1 ]] &&
        abcli_open filename=$filename,$open_options \
            $object_name

    return 0
}
