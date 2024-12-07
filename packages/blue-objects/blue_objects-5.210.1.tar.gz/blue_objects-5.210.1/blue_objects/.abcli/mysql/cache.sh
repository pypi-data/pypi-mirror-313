#! /usr/bin/env bash

function abcli_mysql_cache() {
    local task=$(abcli_unpack_keyword $1 help)
    local keyword=$2

    if [ "$task" == "help" ]; then
        abcli_show_usage "@mysql cache clone$ABCUL<object-1>$ABCUL<object-2>" \
            "clone the mysql cache from <object-1> to <object-2>."

        abcli_show_usage "@mysql cache read$ABCUL<keyword>" \
            "read mysql.cache[<keyword>]."

        abcli_show_usage "@mysql cache search$ABCUL<keyword>" \
            "search in the mysql cache for <keyword>."

        abcli_show_usage "@mysql cache write$ABCUL<keyword> <value>$ABCUL[validate]" \
            "write mysql.cache[<keyword>]=value."
        return
    fi

    if [ "$task" == "clone" ]; then
        python3 -m blue_objects.mysql.cache \
            clone \
            --source "$2" \
            --destination "$3" \
            "${@:4}"
        return
    fi

    if [ "$task" == "read" ]; then
        python3 -m blue_objects.mysql.cache \
            read \
            --keyword "$keyword" \
            "${@:3}"
        return
    fi

    if [ "$task" == "search" ]; then
        python3 -m blue_objects.mysql.cache \
            search \
            --keyword "$keyword" \
            "${@:3}"
        return
    fi

    if [ "$task" == "write" ]; then
        local options=$4
        local do_validate=$(abcli_option_int "$options" "validate" 0)

        python3 -m blue_objects.mysql.cache \
            write \
            --keyword "$keyword" \
            --value "$3" \
            "${@:5}"

        [[ "$do_validate" == 1 ]] &&
            abcli_log "@mysql: cache[$keyword] <- $(abcli_mysql_cache read $keyword)"

        return 0
    fi

    abcli_log_error "@mysql: cache: $task: command not found."
    return 1
}
