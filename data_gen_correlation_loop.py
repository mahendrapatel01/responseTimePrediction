import os
import csv
import time
no_of_records_needed=10000
data_file_name="data.csv"
data_gen_script_template='./data_gen_script.sh {0}'
correlation_script_command='python Correlation_script.py '+data_file_name
csv_file=open(data_file_name,"r")
reader=csv.reader(csv_file,delimiter = ",")
while len(list(reader))<no_of_records_needed:
	no_of_rows=len(list(reader))
	if no_of_rows==0:
		data_gen_script_command=data_gen_script_template.format(True)

	else:
		data_gen_script_command=data_gen_script_template.format(False)

	os.system(data_gen_script_command)
	os.system(correlation_script_command)




	


