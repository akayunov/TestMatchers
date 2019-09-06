#!/usr/bin/env bash

script_dir_name="$( cd "$(dirname "$0")" ; pwd -P )"
#echo $script_dir_name

PYTHONPATH=$script_dir_name/src pytest $script_dir_name/tests
