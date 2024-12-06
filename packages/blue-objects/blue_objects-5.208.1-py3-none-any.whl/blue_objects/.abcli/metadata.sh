#! /usr/bin/env bash

function abcli_metadata() {
    local task=${1:-help}

    local function_name="abcli_metadata_$task"
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "@metadata: $task: command not found."
    return 1
}

abcli_source_caller_suffix_path /metadata
