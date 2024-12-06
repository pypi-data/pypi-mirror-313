#! /usr/bin/env bash

function test_blue_objects_mysql_relations() {
    local object_name_1="test-object-$(abcli_string_timestamp_short)"
    local object_name_2="test-object-$(abcli_string_timestamp_short)"

    local relation=$(abcli mysql relations list --return_list 1 --count 1 --log 0)
    [[ -z "$relation" ]] && return 1

    abcli mysql relations set \
        $object_name_1 \
        $object_name_2 \
        $relation \
        validate
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        $(abcli mysql relations get $object_name_1 $object_name_2 --log 0) \
        $relation
}
