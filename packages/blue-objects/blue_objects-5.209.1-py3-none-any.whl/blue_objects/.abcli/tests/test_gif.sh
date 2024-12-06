#! /usr/bin/env bash

function test_blue_objects_gif() {
    local options=$1

    abcli_gif \
        ~upload,$options \
        $VANWATCH_TEST_OBJECT \
        --frame_duration 200 \
        --output_filename test.gif \
        --scale 2 \
        --suffix .jpg
}
