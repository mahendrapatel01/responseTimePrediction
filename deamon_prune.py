import os
import time

last_line_read=-1
f=open("container_names.txt","r")
f2=open("pruned_container_names.txt","a+")
docker_stop_template="docker container stop {0}"
docker_rm_template="docker container rm {0}"

while True:
	f.seek(0,0)
	lines=f.readlines()
	# print(lines)
	if (len(lines)-1)<=last_line_read:
		continue
	container_name=lines[last_line_read+1][:-1]
	last_line_read+=1
	docker_stop_command=docker_stop_template.format(container_name)
	docker_rm_command=docker_rm_template.format(container_name)
	os.system(docker_stop_command)
	os.system(docker_rm_command)
	with open("pruned_container_names.txt","a+") as f2:
		f2.write(container_name+"\n")
		f2.close()


