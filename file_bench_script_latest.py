import os

import pandas as pd

import itertools

import time

import re

import json

import sys

import csv

import argparse

ap = argparse.ArgumentParser()

ap.add_argument("--data", required=True, help="Data file name")

ap.add_argument("--input-params", required=True, help="Input json file name")

ap.add_argument("--isDataEmpty",default=False, help="Field to say whether data file is empty or not")

args = vars(ap.parse_args())

data_file=args["data"]
input_params_file=args["input_params"]
is_data_empty=args["isDataEmpty"]


"""
if len(sys.argv)<4:
	sys.exit("Enter valid number of parameters")
"""
f= open(input_params_file)

input_params=json.load(f)

docker_cpus=input_params["noOfCpus"]

docker_memories=input_params["memories"]

docker_iorate_limits=input_params["ioRateLimits"]

filesizes=input_params["fileSizes"]

iosizes=input_params["ioSizes"]

nthreads=input_params["noOfThreads"]

memsizes=input_params["threadMemories"]

container_command_template='docker run --privileged --name={0} --cpus={1}  --memory={2} --device-write-bps /dev/sda:{3} -dit krshailesh/filebench_cs681'
docker_exec_template='docker exec -i {0} {1}'

sed_command_template='sed -i -e "s/filesize=[0-9a-z]\+/filesize={0}/gm" -e "s/iosize=[0-9a-z]\+/iosize={1}/gm" -e "s/nthreads=[0-9a-z]\+/nthreads={2}/gm" -e "s/memsize=[0-9a-z]\+/memsize={3}/gm"   randomwrite.f'

docker_cp_command_template='docker cp randomwrite.f {0}:/home/randomwrite.f'

filebench_command='/bin/bash -c "echo 0 > /proc/sys/kernel/randomize_va_space;filebench -f /home/randomwrite.f"'


inp_data=itertools.product(docker_cpus,docker_memories,docker_iorate_limits,filesizes,iosizes,nthreads,memsizes)

df = pd.DataFrame(inp_data)

grouped_docker_params=list(df.groupby([0,1,2]))

data_rows=[]

data_header_row=["NoOfCpus","Memory","IoRateLimits(mb/sec)","FileSize","IoSize","NoOfThreads","ThreadMemory","ResponseTime(msec/op)","Throughput(op/sec)"]

# container_names_file=open("container_names.txt","a+")
counter=0

# csv_file=open(sys.argv[2],"a+")
# reader_file_obj = csv.reader(csv_file)
# writer_file_obj = csv.writer(csv_file)
# if len(list(reader_file_obj))==0:
	# writer_file_obj.writerow(data_header_row)

flag=True

for grouped_docker_param in grouped_docker_params:
	filebench_params = [tuple(x)[3:] for x in grouped_docker_param[1].to_numpy()]
	cpus_to_be_alloted=grouped_docker_param[0][0]
	memory_to_be_alloted=grouped_docker_param[0][1]
	iorate_to_be_limited=grouped_docker_param[0][2]
	container_name="container_"+str(cpus_to_be_alloted)+"_"+memory_to_be_alloted+"_"+iorate_to_be_limited
	container_command=container_command_template.format(container_name,cpus_to_be_alloted,memory_to_be_alloted,iorate_to_be_limited)
	#print(container_command)
	os.system(container_command)
	data_rows=[]
	for filebench_param in filebench_params:
		#print(str(filebench_param))
		sed_command=sed_command_template.format(filebench_param[0],filebench_param[1],filebench_param[2],filebench_param[3])
		os.system(sed_command)
		print(sed_command)
		docker_cp_command=docker_cp_command_template.format(container_name)
		os.system(docker_cp_command)
		docker_exec_command=docker_exec_template.format(container_name,filebench_command)
		#print(docker_exec_command)
		out=os.popen(docker_exec_command).read()
		#print(out)
		lines=out.splitlines()
		summary_line=""
		for line in lines:
			if re.search("IO Summary",line):
				summary_line=line
				break;
		print(summary_line)
		vals=summary_line.split()
		if len(vals)>0:
			response_time_val=re.findall(r'-?\d+\.?\d*',vals[-1])[0]
			print(response_time_val)
			through_put_val=vals[5]
			print(through_put_val)
		# time.sleep(1800)
			data_row=[cpus_to_be_alloted,memory_to_be_alloted,iorate_to_be_limited,filebench_param[0],filebench_param[1],filebench_param[2],filebench_param[3],response_time_val,through_put_val]
			data_rows.append(data_row)
	with open(data_file,"a+") as csv_file:
		writer_file_obj = csv.writer(csv_file)
		if is_data_empty and flag:
			writer_file_obj.writerow(data_header_row)
			flag=False
		writer_file_obj.writerows(data_rows)
		csv_file.close()
	with open("container_names.txt","a+") as container_names_file:
		container_names_file.write(container_name+"\n")
		container_names_file.close()
	
		

"""
csv_file=open(sys.argv[2],"a+")
reader_file_obj = csv.reader(csv_file)
writer_file_obj = csv.writer(csv_file)
if len(list(reader_file_obj))==0:
	writer_file_obj.writerow(data_header_row)

writer_file_obj.writerows(data_rows)
"""