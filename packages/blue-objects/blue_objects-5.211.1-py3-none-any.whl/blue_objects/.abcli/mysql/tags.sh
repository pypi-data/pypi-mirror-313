#! /usr/bin/env bash

export abcli_tag_search_args="[--count <count>]$ABCUL[--delim space]$ABCUL[--log 0]$ABCUL[--offset <offset>]"

function abcli_mysql_tags() {
    local task=$(abcli_unpack_keyword $1 help)
    local object=$(abcli_clarify_object $2 .)

    if [ "$task" == "help" ]; then
        abcli_show_usage "@mysql tags clone$ABCUL<object-1>$ABCUL<object-2>" \
            "clone <object-1> mysql tags -> <object-2>."

        abcli_show_usage "@mysql tags get$ABCUL<object-name>" \
            "get <object-name> mysql tags."

        abcli_show_usage "@mysql tags search$ABCUL<tag>$ABCUL$abcli_tag_search_args" \
            "search for all objects that are tagged tag in mysql."

        abcli_show_usage "@mysql tags set$ABCUL<object-1,object-2>$ABCUL<tag-1,~tag-2>$ABCUL[validate]" \
            "add <tag-1> and remove <tag-2> from <object-1> and <object-2> in mysql."

        abcli_show_usage "@mysql tags set${ABCUL}disable|enable" \
            "disable|enable '@mysql tags set'."
        return
    fi

    if [ "$task" == "clone" ]; then
        python3 -m blue_objects.mysql.tags \
            clone \
            --object $object \
            --object_2 $(abcli_clarify_object $3 .) \
            "${@:4}"
        return
    fi

    if [ "$task" == "get" ]; then
        python3 -m blue_objects.mysql.tags \
            get \
            --item_name tag \
            --object $object \
            "${@:3}"
        return
    fi

    if [ "$task" == "search" ]; then
        python3 -m blue_objects.mysql.tags \
            search \
            --tags $2 \
            "${@:3}"
        return
    fi

    if [ "$task" == "set" ]; then
        if [ "$object" == "disable" ]; then
            export ABCLI_TAG_DISABLE=true
            return
        elif [ "$object" == "enable" ]; then
            export ABCLI_TAG_DISABLE=false
            return
        elif [ "$ABCLI_TAG_DISABLE" == true ]; then
            abcli_log_warning "ignored '@mysql tags set ${@:2}'."
            return
        fi

        local options=$4
        local do_validate=$(abcli_option_int "$options" validate 0)

        local object
        for object in $(echo "$object" | tr , " "); do
            python3 -m blue_objects.mysql.tags \
                set \
                --object $object \
                --tags $3 \
                "${@:5}"

            [[ "$do_validate" == 1 ]] &&
                abcli_log "mysql: $object: $(abcli_mysql_tags get $object --log 0)"
        done

        return 0
    fi

    abcli_log_error "@mysql: tags: $task: command not found."
    return 1
}
