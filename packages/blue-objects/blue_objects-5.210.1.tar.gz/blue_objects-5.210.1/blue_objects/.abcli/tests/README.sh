#! /usr/bin/env bash

function test_blue_objects_README() {
    local options=$1

    abcli_eval ,$options \
        blue_objects build_README
}
