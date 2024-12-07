#! /usr/bin/env bash

function test_blue_objects_mysql_tags() {
    local object_name="test-object-$(abcli_string_timestamp_short)"
    local tag="test-tag-$(abcli_string_timestamp_short)"

    abcli mysql tags set \
        $object_name \
        $tag \
        validate
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        $(abcli mysql tags get $object_name --log 0) \
        $tag
}
