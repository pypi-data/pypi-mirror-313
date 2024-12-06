#! /usr/bin/env bash

function test_blue_objects_mlflow_cache() {
    local keyword="test-keyword-$(abcli_string_timestamp_short)"
    local value="test-value-$(abcli_string_timestamp_short)"

    abcli mlflow cache write \
        $keyword $value
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        $(abcli mlflow cache read $keyword) \
        $value
}
