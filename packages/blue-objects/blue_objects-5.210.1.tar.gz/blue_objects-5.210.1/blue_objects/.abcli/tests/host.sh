#! /usr/bin/env bash

function test_blue_objects_host() {
    abcli_assert \
        $(abcli_host get name) \
        - non-empty
}
