import sys
import pandas 
import numpy
import json
import math

def gToActual(x):
    x = str(x)
    if(x[-1]=='k'):
        return int(int(x[:-1],10)*1024)
    elif(x[-1]=='m'):
        return int(int(x[:-1],10)*1024*1024)
    elif(x[-1]=='g'):
        return int(int(x[:-1],10)*1024*1024*1024)
    return int(x,10)

def gbToActual(x):
    x = str(x)
    if(x[-2:]=='kb'):
        return int(int(x[:-2],10)*1024)
    elif(x[-2:]=='mb'):
        return int(int(x[:-2],10)*1024*1024)
    elif(x[-2:]=='gb'):
        return int(int(x[:-2],10)*1024*1024*1024)
    return int(x,10)
    
def actualTog(x):
    x = int(x)
    if(x>=1024*1024*1024):
        return str(int(x/(1024*1024*1024)))+'g'
    elif(x>=1024*1024):
        return str(int(x/(1024*1024)))+'m'
    elif(x>=1024):
        return str(int(x/1024))+'k'
    return str(int(x))

def actualTogb(x):
    x = int(x)
    if(x>=1024*1024*1024):
        return str(int(x/(1024*1024*1024)))+'gb'
    elif(x>=1024*1024):
        return str(int(x/(1024*1024)))+'mb'
    elif(x>=1024):
        return str(int(x/1024))+'kb'
    return str(int(x))

def removeG(x):
    return int(str(x[:-1]))

def removeMb(x):
    return int(str(x[:-2]))

def addG(x):
    return str(x)+'g'

def addK(x):
    return str(x)+'k'

def addMb(x):
    return str(x)+'mb'
    
n = len(sys.argv)

if(n<2):
    print("invalid command, enter input csv filename")
    sys.exit()

# reading data from csv
data = pandas.read_csv(sys.argv[1])
print(data)

# processing for input data
data['Memory']=data['Memory'].apply(removeG)
data['FileSize'] = data['FileSize'].apply(gToActual)
data['IoSize'] = data['IoSize'].apply(removeG)
data['ThreadMemory'] = data['ThreadMemory'].apply(gToActual)
data['IoRateLimits(mb/sec)'] = data['IoRateLimits(mb/sec)'].apply(removeMb)

data = data.drop(columns='Throughput(op/sec)')

print(data)
data.to_csv("data_1300_rows_unitless.csv")
# data.to_csv("data5.csv")
# finding correlation

NO_OF_CORRELATED_COLUMN=3

correlation_vector = []
for col in data.columns:
    corr= abs(data['ResponseTime(msec/op)'].corr(data[col]))
    if(not math.isnan(corr)):
        correlation_vector.append(corr)
    else:
        correlation_vector.append(0)
    
top3_correlated_values =  sorted(correlation_vector[:-1])[-3:]   
max_inds = []
for val in top3_correlated_values:
    max_inds.append(correlation_vector.index(val))

max_cols=[]
for i in max_inds:
    max_cols.append(data.columns[i])
print(max_inds)
print(max_cols)

"""
col= sorted(data[max_col].unique())
new_col=[]
# new_col.append(data[data.columns[ind]][0])
for i in range(1,len(col)):
    new_col.append(math.ceil((col[i-1]+col[i])/2))
"""

# calculating high correlated columns new rows


# saving in json    
output_data={}

for coln in data.columns:
    output_data[coln]=sorted(data[coln].unique())
    
new_cols={}
for max_col in max_cols:
    new_cols[max_col] = []
    for i in range(1,len(output_data[max_col])):
        new_cols[max_col].append(math.ceil((output_data[max_col][i-1]+output_data[max_col][i])/2))

output_data['memories']=[addG(x) for x in output_data['Memory']]
del output_data['Memory']
output_data['fileSizes'] = [actualTog(x) for x in output_data['FileSize']]
del output_data['FileSize']
output_data['ioSizes'] = [addK(x) for x in output_data['IoSize']]
del output_data['IoSize']
output_data['threadMemories'] = [actualTog(x) for x in output_data['ThreadMemory']]
del output_data['ThreadMemory']
output_data['ioRateLimits'] = [addMb(x) for x in output_data['IoRateLimits(mb/sec)']]
del output_data['IoRateLimits(mb/sec)']

output_data['noOfThreads'] = output_data['NoOfThreads']
del output_data['NoOfThreads']


# print(output_data)
for max_col in max_cols:

    max_col2= max_col
    if(max_col == 'Memory'):
        max_col = 'memories'
    elif(max_col == 'FileSize'):
        max_col = 'fileSizes'
    elif(max_col == 'IoSize'):
        max_col = 'ioSizes'
    elif(max_col == 'ThreadMemory'):
        max_col = 'threadMemories'
    elif(max_col == 'IoRateLimits(mb/sec)'):
        max_col = 'ioRateLimits'
    elif(max_col == 'NoOfCpus'):
        max_col = 'noOfCpus'
    elif(max_col == 'NoOfThreads'):
        max_col = 'noOfThreads'

        
    # output_data[max_col] = new_col 
    output_data[max_col] = [str(int(x)) for x in new_cols[max_col2]]
    output_data['noOfThreads'] = [str(int(x)) for x in output_data['noOfThreads']]
    if(max_col == 'memories'):
        output_data['memories']=[addG(x) for x in new_cols[max_col2]]
    elif(max_col == 'fileSizes'):
        output_data['fileSizes']=[actualTog(x) for x in new_cols[max_col2]]
    elif(max_col == 'ioSizes'):
        output_data['ioSizes']=[addK(x) for x in new_cols[max_col2]]
    elif(max_col == 'threadMemories'):
        output_data['threadMemories']=[actualTog(x) for x in new_cols[max_col2]]
    elif(max_col == 'ioRateLimits'):
        output_data['ioRateLimits']=[addMb(x) for x in new_cols[max_col2]]

    print(output_data[max_col])
# output_data[max_col] = [str(int(x)) for x in output_data[max_col]] 
output_data['noOfCpus'] = [str(int(x)) for x in output_data['NoOfCpus']] 
del output_data['NoOfCpus']
    
del output_data['ResponseTime(msec/op)']
print(output_data)

with open("input_params.json", "w") as outfile: 
    json.dump(output_data, outfile,indent=2)
    
    
    
    
    
    
    
    
