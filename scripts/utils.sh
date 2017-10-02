#!/bin/bash

print_empty_line()
{
    echo ""
}

print_dict()
{
    arr=$1
    for key in ${!arr[@]}; do
        echo ${key} ${arr[${key}]}
    done
}
