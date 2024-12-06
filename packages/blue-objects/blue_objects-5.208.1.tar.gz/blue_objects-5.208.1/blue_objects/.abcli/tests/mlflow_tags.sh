#! /usr/bin/env bash

function test_blue_objects_mlflow_tags_validation() {
    local object_name="test-object-$(abcli_string_timestamp_short)"
    local tag="test-tag-$(abcli_string_timestamp_short)"
    local value="test-value-$(abcli_string_timestamp_short)"

    abcli mlflow tags set \
        $object_name \
        $tag=$value
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        "$(abcli mlflow tags get $object_name --tag $tag)" \
        $value
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        "$(abcli mlflow tags get $object_name --tag some-tag)" \
        - empty
}

function test_blue_objects_mlflow_tags_search() {
    local options=$1

    abcli_mlflow_tags search \
        cloned.firms_area-template-v1=True \
        --log 0
}
