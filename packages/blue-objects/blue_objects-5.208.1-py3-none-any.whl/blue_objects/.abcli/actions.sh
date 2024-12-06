#! /usr/bin/env bash

function blue_objects_action_git_before_push() {
    blue_objects build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    blue_objects pypi build
}
