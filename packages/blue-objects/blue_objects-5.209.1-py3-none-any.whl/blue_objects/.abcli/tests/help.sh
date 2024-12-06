#! /usr/bin/env bash

function test_blue_objects_help() {
    # TODO: enable
    return 0

    local options=$1

    local module
    for module in \
        "@objects" \
        \
        "@objects pypi" \
        "@objects pypi browse" \
        "@objects pypi build" \
        "@objects pypi install" \
        \
        "@objects pytest" \
        \
        "@objects test" \
        "@objects test list" \
        \
        "abcli cache" \
        \
        "@cp" \
        \
        "@download" \
        \
        "@gif" \
        \
        "abcli host" \
        \
        "abcli metadata" \
        \
        "@mlflow" \
        "@mlflow browse" \
        "@mlflow cache" \
        "@mlflow get_id" \
        "@mlflow get_run_id" \
        "@mlflow list_registered_models" \
        "@mlflow log_artifacts" \
        "@mlflow log_run" \
        "@mlflow rm" \
        "@mlflow run" \
        "@mlflow tags" \
        "@mlflow tags clone" \
        "@mlflow tags get" \
        "@mlflow tags search" \
        "@mlflow tags set" \
        "@mlflow test" \
        "@mlflow transition" \
        \
        "abcli mysql" \
        "abcli mysql_cache" \
        "abcli mysql_relations" \
        "abcli mysql_tags" \
        \
        "abcli object" \
        "abcli publish" \
        "abcli select" \
        "abcli storage" \
        "abcli tags" \
        "abcli upload" \
        \
        "blue_objects"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
