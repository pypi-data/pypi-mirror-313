#! /usr/bin/env bash

function test_blue_objects_ls() {
    abcli_select

    abcli_upload

    abcli_ls cloud

    abcli_ls local

    abcli_ls "$abcli_path_bash/tests/*.sh"
}
