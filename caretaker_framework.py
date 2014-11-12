############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       10/20/2014       ##
## caretaker_framework.py ##
##         v1.0           ##
############################

import subprocess
from gaussjob import *
from last20 import *

## creating an sqjobs.txt file to work with

job_object = open('sqjobs.txt','w')
sqjobs_call = subprocess.call(['sqjobs'],shell=True,stdout=job_object)
job_object.close()

print "'sqjobs.txt' created in current directory"

"""
 An 'sqjobs.txt' data processing hub. Reads all jobs found in 'sqjobs.txt' and
 stores the data in gaussjob_dict [where {jobid : gaussjob object}]. Jobs are
 stored uniquely by the jobid assigned by SHARCNET. 
 Also produces a second database state_dict [where {state: [jobIDs(state)]}].
"""

# open the text file containing sharcnet gaussian gob filedata info
fo = open('sqjobs.txt', "rw+")
lines = fo.readlines()

# this segment of code removes any '\n' or other book-keeping strings
stripped_filedata = []
for k in range(0,len(lines)):
    stripped_filedata.append(lines[k].strip())

# close the text file     
fo.close()

# create a new dictionary where {jobid : gaussjob object}
gaussjob_dict = {}

# number of information lines at top of the file
n_infolines = 2
for i in range(n_infolines,len(stripped_filedata)):
    job = stripped_filedata[i].split()
    # check if sharcnet provides information about node
    node_bool = len(job)==7
    if node_bool:
        job.insert(4,'')
    
    # create a gaussjob object in gaussjob_dict
    gaussjob_dict[job[0]] = gaussjob(job[0],job[1],job[2],job[3],job[4],job[5],job[6],job[7],)

# create a master copy of all jobIDs for dictionary indexing purposes    
job_IDs = gaussjob_dict.keys()

# create a job state dictionary where {state: [jobIDs(state)]}
state_dict = {'D':[],'Q':[],'R':[]}

# add jobIDs to their respective state
for i in range(0,len(job_IDs)):
    jobstatus = gaussjob_dict[job_IDs[i]].state
    state_dict[jobstatus].append(gaussjob_dict[job_IDs[i]].filename)
    
##print('Finished jobIDs:')
##print(state_dict['D'])
##print('Running jobIDs:')
##print(state_dict['R'])
##print('Queued jobIDs:')
##print(state_dict['Q'])


for i in state_dict['D']:
    print i
    if gauss_terminate_line(last20(i)) == 'walltime':
        print 'walltime on file: ' + i


