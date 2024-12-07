#! /usr/bin/env bash

function test_blue_objects_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_objects version ${@:2}"

    return 0
}


