############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       10/20/2014       ##
## caretaker_framework.py ##
##         v1.1           ##
############################

import subprocess
from gaussjob import *
from last20 import *

## creating an sqjobs.txt file to work with

job_object = open('sqjobs.txt','w')
sqjobs_call = subprocess.call(['sqjobs -l'],shell=True,stdout=job_object)
job_object.close()

print "'sqjobs.txt' created in current directory"

"""
 An 'sqjobs.txt' data processing hub. Reads all jobs found in 'sqjobs.txt' and
 stores the data in gaussjob_dict [where {jobid : gaussjob object}]. Jobs are
 stored uniquely by the jobid assigned by SHARCNET. 
 Also produces a second database state_dict [where {state: [jobIDs(state)]}].
"""

# open the text file containing sharcnet gaussian gob filedata info
fo = open('sqjobs.txt', "r")
lines = fo.readlines()

# this segment of code removes any '\n' or other book-keeping strings
stripped_filedata = []
for k in range(0,len(lines)):
    stripped_filedata.append(lines[k].strip())

# close the text file     
fo.close()

# create a new dictionary where {jobid : gaussjob object}
gaussjob_dict = {}

## updated gaussjob class implementation and more detailed sqjobs.txt
#print stripped_filedata
index = 0
while index < len(stripped_filedata) - 1:
    line = stripped_filedata[index].split()
    if line == ['key', 'value']:
        index += 2
        line = stripped_filedata[index].split()
        job_id = line[1]
        gaussjob_dict[job_id] = gaussjob()
        gaussjob_dict[job_id].jobid = job_id
        index += 1
        line = stripped_filedata[index].split()
        while index < len(stripped_filedata) - 1 and line != ['key', 'value']:
            if line == []:
                pass
            elif line[0] == 'out' and line[1]=='file:':
                gaussjob_dict[job_id].filename = line[-1].split('/')[-1]
            elif line[0] == 'state:':
                gaussjob_dict[job_id].state = line[1]
            elif line[0] == 'Job' and line[1] == 'died':
                gaussjob_dict[job_id].walltime = True
            index += 1
            line = stripped_filedata[index].split()
        print gaussjob_dict[job_id]

## number of information lines at top of the file
#n_infolines = 2
#for i in range(n_infolines,len(stripped_filedata)):
    #job = stripped_filedata[i].split()
    ## check if sharcnet provides information about node
    #node_bool = len(job)==7
    #if node_bool:
        #job.insert(4,'')
    
    ## create a gaussjob object in gaussjob_dict
    #gaussjob_dict[job[0]] = gaussjob(job[0],job[1],job[2],job[3],job[4],job[5],job[6],job[7],)

# create a master copy of all jobIDs for dictionary indexing purposes    
job_IDs = gaussjob_dict.keys()

print len(job_IDs)

# create a job state dictionary where {state: [jobIDs(state)]}
state_dict = {'D':[],'Q':[],'R':[]}

# add jobIDs to their respective state
for i in range(0,len(job_IDs)):
    jobstatus = gaussjob_dict[job_IDs[i]].state
    state_dict[jobstatus].append(gaussjob_dict[job_IDs[i]].jobid)
    
print 'Finished Job_IDs:'
for job in state_dict['D']:
    print job
print 'Running filenames:'
for job in state_dict['R']:
    print job
print 'Queued filenames:'
for job in state_dict['Q']:
    print job



done_jobids = state_dict['D']


walltime_resubs = []

x= input('Specify a runtime:')

for i in done_jobids:
    if gaussjob_dict[i].walltime:
        walltime_resubs.append('sqsub -q threaded -n 8 -r ' + str(x) + ' --mpp=5g -o ' + gaussjob_dict[i].filename + ' g09 ' + gaussjob_dict[i].filename[:-3] + 'gjf' + '\n')
	#print walltime_resubs
        print 'i found a walltime'
    else:
        print 'no walltime on filename: ' + gaussjob_dict[i].filename

print walltime_resubs

fo = open('sqsub_batch_resub', 'w')
fo.writelines(walltime_resubs)
fo.close()

#Little piece to find a delete duplicates before submitting the files to the Queue
with open('sqsub_batch_resub.txt', 'r') as f:
    files_batch_sqsub_list = [line.strip() for line in f]
    print set(files_batch_sqsub_list) #set funciton goes through list returns only unique values
    # I don't know wheteher I can close the files or have it overwrite at this stage 
    

#subprocess.call(['chmod 757 sqsub_batch_resub'],shell=True)
#subprocess.call(['./sqsub_batch_resub'],shell=True)


