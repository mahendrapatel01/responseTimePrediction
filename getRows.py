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
data = pandas.read_csv('data4.csv')
print(data)

# processing for input data
data['Memory']=data['Memory'].apply(removeG)
data['FileSize'] = data['FileSize'].apply(gToActual)
data['IoSize'] = data['IoSize'].apply(removeG)
data['ThreadMemory'] = data['ThreadMemory'].apply(gToActual)
data['IoRateLimits(mb/sec)'] = data['IoRateLimits(mb/sec)'].apply(removeMb)

data = data.drop(columns='Throughput(op/sec)')

print(data)

# data.to_csv("data5.csv")
# finding correlation
arr = []
for col in data.columns:
    corr= abs(data['ResponseTime(msec/op)'].corr(data[col]))
    if(not math.isnan(corr)):
        arr.append(corr)
    else:
        arr.append(0)
    
max_ind = arr.index(max(arr[:-1]))
max_col = data.columns[max_ind]
print(max_ind)
print(max_col)
col= sorted(data[max_col].unique())
new_col=[]
# new_col.append(data[data.columns[ind]][0])
for i in range(1,len(col)):
    new_col.append((col[i-1]+col[i])/2)


# calculating high correlated columns new rows


# saving in json    
data2={}
for coln in data.columns:
    data2[coln]=sorted(data[coln].unique())
    
new_col=[]
for i in range(1,len(data2[max_col])):
    new_col.append((data2[max_col][i-1]+data2[max_col][i])/2)
    
data2['memories']=[addG(x) for x in data2['Memory']]
del data2['Memory']
data2['fileSizes'] = [actualTog(x) for x in data2['FileSize']]
del data2['FileSize']
data2['ioSizes'] = [addK(x) for x in data2['IoSize']]
del data2['IoSize']
data2['threadMemories'] = [actualTog(x) for x in data2['ThreadMemory']]
del data2['ThreadMemory']
data2['ioRateLimits'] = [addMb(x) for x in data2['IoRateLimits(mb/sec)']]
del data2['IoRateLimits(mb/sec)']

data2['noOfThreads'] = data2['NoOfThreads']
del data2['NoOfThreads']


# print(data2)
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

    
    
# data2[max_col] = new_col 
data2[max_col] = [str(int(x)) for x in new_col]
data2['noOfThreads'] = [str(int(x)) for x in data2['noOfThreads']]
if(max_col == 'memories'):
    data2['memories']=[addG(x) for x in new_col]
elif(max_col == 'fileSizes'):
    data2['fileSizes']=[actualTog(x) for x in new_col]
elif(max_col == 'ioSizes'):
    data2['ioSizes']=[addK(x) for x in new_col]
elif(max_col == 'threadMemories'):
    data2['threadMemories']=[actualTog(x) for x in new_col]
elif(max_col == 'ioRateLimits'):
    data2['ioRateLimits']=[addMb(x) for x in new_col]

print(data2[max_col])
# data2[max_col] = [str(int(x)) for x in data2[max_col]] 
data2['noOfCpus'] = [str(int(x)) for x in data2['NoOfCpus']] 
del data2['NoOfCpus']
    
del data2['ResponseTime(msec/op)']
print(data2)
with open("output.json", "w") as outfile: 
    json.dump(data2, outfile,indent=2)
    
    
    
    
    
    
    
    

