#! /usr/bin/env bash

function test_blue_objects_mlflow_logging() {
    local object_name="test-object-$(abcli_string_timestamp_short)"

    abcli clone \
        upload \
        vanwatch-mlflow-validation-2024-09-23-10673 \
        "$object_name"

    abcli_mlflow rm $object_name
}
