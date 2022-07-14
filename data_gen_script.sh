#!/bin/bash
if [[ -z "$1" ]]; then
	initial_data="False"
else
	initial_data=$1
fi

trap sigint_handler SIGINT

sigint_handler()
{

sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in "cd PA3_CS681; cat data.csv" > data.csv
sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in  "ps -ef | grep -v grep | grep deamon_prune.py | awk '{print \$2}' | xargs kill"
exit

}

sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in "cat /dev/null > PA3_CS681/container_names.txt;cat /dev/null > PA3_CS681/pruned_container_names.txt"
sshpass -f password_file scp input_params.json chaitanyavarma@sl1-22.cse.iitb.ac.in:/users/pg20/chaitanyavarma/PA3_CS681/
sshpass -f password_file scp data.csv chaitanyavarma@sl1-22.cse.iitb.ac.in:/users/pg20/chaitanyavarma/PA3_CS681/
sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in "cd PA3_CS681; python3 deamon_prune.py" &
sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in "cd PA3_CS681; python3 file_bench_script_latest.py --data data.csv --input-params input_params.json --isDataEmpty=$initial_data"
sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in "cd PA3_CS681; cat data.csv" > data.csv
sshpass -f password_file ssh chaitanyavarma@sl1-22.cse.iitb.ac.in  "ps -ef | grep -v grep | grep deamon_prune.py | awk '{print \$2}' | xargs kill"

