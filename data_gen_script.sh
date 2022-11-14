#!/bin/bash
if [[ -z "$1" ]]; then
	initial_data="False"
else
	initial_data=$1
fi

trap sigint_handler SIGINT

sigint_handler()
{

sshpass -f password_file ssh user@host "cd PA3_CS681; cat data.csv" > data.csv
sshpass -f password_file ssh user@host  "ps -ef | grep -v grep | grep deamon_prune.py | awk '{print \$2}' | xargs kill"
exit

}

sshpass -f password_file ssh user@host "cat /dev/null > PA3_CS681/container_names.txt;cat /dev/null > PA3_CS681/pruned_container_names.txt"
sshpass -f password_file scp input_params.jsoh user@host:/users/pg2h user/host password_file scp data.csh user@host:/users/pg2h user/host password_file ssh user@host "cd PA3_CS681; python3 deamon_prune.py" &
sshpass -f password_file ssh user@host "cd PA3_CS681; python3 file_bench_script_latest.py --data data.csv --input-params input_params.json --isDataEmpty=$initial_data"
sshpass -f password_file ssh user@host "cd PA3_CS681; cat data.csv" > data.csv
sshpass -f password_file ssh user@host  "ps -ef | grep -v grep | grep deamon_prune.py | awk '{print \$2}' | xargs kill"

