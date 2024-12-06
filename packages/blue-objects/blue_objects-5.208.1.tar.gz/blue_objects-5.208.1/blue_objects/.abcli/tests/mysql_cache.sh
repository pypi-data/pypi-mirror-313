#! /usr/bin/env bash

function test_blue_objects_mysql_cache() {
    local keyword="test-keyword-$(abcli_string_timestamp_short)"
    local value="test-value-$(abcli_string_timestamp_short)"

    abcli mysql cache write \
        $keyword $value \
        validate
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        $(abcli mysql cache read $keyword) \
        $value
}
