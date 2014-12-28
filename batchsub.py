############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       11/24/2014       ##
##      batchsub.py       ##
##         v1.0           ##
############################

import os

print 'Creating filedir.txt'
os.system('ls *.gjf > filedir')

fo = open('filedir')
input_filenames = fo.readlines()
fo.close

l_write = []
for i in range(len(input_filenames)):
    temp = input_filenames[i].split('.')[0]
    l_write.append('sqsub -q threaded --mpp=12g -n 8 -r 2d -o ' + temp + '.log g09 ' + temp + '.gjf\n')

fw = open('nlgn_batchsub','w')
fw.writelines(l_write)
fw.close()

if len(l_write) > 0:
    print 'The following is a sample job submission:'
    print l_write[0]
    if raw_input('Is this correct? [y,n]: ') == 'y':
        if raw_input('Submit ' + str(len(l_write)) + ' jobs? [y,n]: ') == 'y':
            os.system('chmod 757 nlgn_batchsub')
            os.system('./nlgn_batchsub')
