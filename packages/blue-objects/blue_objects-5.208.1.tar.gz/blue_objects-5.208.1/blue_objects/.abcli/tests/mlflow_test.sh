#! /usr/bin/env bash

function test_blue_objects_mlflow_test() {
    local options=$1

    abcli_mlflow_test "$@"
}
