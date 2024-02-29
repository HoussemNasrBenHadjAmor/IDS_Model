#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # On the same directory.

script_csv_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/csv" 

script_nb_rows_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/rows" 

latest_file_path=$script_csv_dir/$(ls $script_csv_dir -lt --time=creation | grep '.*\.csv' | head -n 1 | awk '{print$9}')

latest_nb_rows_path=

nb_rows_exist=$(find $script_nb_rows_dir -maxdepth 1 -type f -name "*.txt" -newermt $(date +%Y-%m-%d) ! -newermt $(date -d tomorrow +%Y-%m-%d) | head -n 1)


if [ -n "$nb_rows_exist" ]; then
    latest_nb_rows_path=$nb_rows_exist
else
    latest_nb_rows_path=$script_nb_rows_dir
fi

#latest_nb_rows_path=$script_nb_rows_dir$(ls $script_nb_rows_dir -lt --time=creation | grep '.*\.txt' | head -n 1 | awk '{print$9}')

#latest_nb_rows_path=$script_nb_rows_dir$(find $script_nb_rows_dir -maxdepth 1 -type f -name "*.txt" -newermt $(date +%Y-%m-%d) ! -newermt $(date -d tomorrow +%Y-%m-%d) | head -n 1)

model_path="$script_dir/CNN.h5"
encoder_path="$script_dir/le.joblib"



post_rotate_command="python3 ${script_dir}/classification.py ${script_dir} ${latest_file_path} ${latest_nb_rows_path} ${model_path} ${encoder_path}"

$post_rotate_command

