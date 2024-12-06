#! /usr/bin/env bash

function abcli_upload() {
    local options=$1
    local filename=$(abcli_option "$options" filename)
    local do_open=$(abcli_option_int "$options" open 1)
    local do_solid=$(abcli_option_int "$options" solid 0)
    local warn_if_exists=$(abcli_option_int "$options" warn_if_exists 1)
    local log_to_mlflow=$(abcli_option_int "$options" mlflow 0)
    local no_mlflow=$(abcli_option_int "$options" no_mlflow 0)

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    # https://stackoverflow.com/a/45200066
    local exists=$(aws s3 ls $ABCLI_AWS_S3_BUCKET_NAME/$ABCLI_AWS_S3_PREFIX/$object_name.tar.gz)
    if [ ! -z "$exists" ]; then
        if [[ "$warn_if_exists" == 1 ]]; then
            abcli_log_warning "@abcli: upload: $object_name.tar.gz already exists on the cloud, use \"abcli object open\" to open the object."
        else
            abcli_log "✅ ☁️  $object_name.tar.gz."
        fi
        return
    fi

    rm -rf $object_path/auxiliary

    if [ ! -z "$filename" ]; then
        local file_size=$(blue_objects_file size $filename)
        abcli_log "uploading $object_name/$filename ($file_size) ..."

        aws s3 cp \
            $object_path/$filename \
            $ABCLI_S3_OBJECT_PREFIX/$object_name/

        return
    fi

    if [ "$do_open" == 1 ]; then
        abcli_log "uploading $object_name ..."

        aws s3 sync \
            $object_path/ \
            $ABCLI_S3_OBJECT_PREFIX/$object_name/

        abcli_tags set $object_name open
    fi

    if [ "$do_solid" == 1 ]; then
        pushd $ABCLI_OBJECT_ROOT >/dev/null

        tar -czvf \
            $object_name.tar.gz \
            ./$object_name

        local object_size=$(blue_objects_file size $object_path.tar.gz)
        abcli_log "uploading $object_name.tar.gz ($object_size) ..."

        aws s3 cp \
            $object_name.tar.gz \
            $ABCLI_S3_OBJECT_PREFIX/

        abcli_tags set $object_name solid

        popd >/dev/null
    fi

    if [[ "$log_to_mlflow" == 1 ]]; then
        abcli_mlflow log_artifacts $object_name
    elif [[ "$no_mlflow" == 0 ]]; then
        abcli_mlflow log_run $object_name
    fi
}
