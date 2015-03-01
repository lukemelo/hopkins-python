############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       11/24/2014       ##
##      batchsub.py       ##
##         v2.0           ##
############################

import os

print 'Creating filedir.txt'
os.system('ls *.gjf > filedir')
fo = open('filedir')
input_filenames = fo.readlines()
fo.close
os.system('rm filedir')

l_write = []
for i in range(len(input_filenames)):
    temp = input_filenames[i].split('.')[0]
	## dedicated queue NRAP_878
    l_write.append('sqsub -q NRAP_878 -f threaded --mpp=8g -n 8 -r 4d -o ' + temp + '.log g09 ' + temp + '.gjf\n')
	## normal queue
    #l_write.append('sqsub -q threaded --mpp=8g -n 8 -r 4d -o ' + temp + '.log g09 ' + temp + '.gjf\n')

fw = open('batchsub','w')
fw.writelines(l_write)
fw.close()

if len(l_write) > 0:
    print 'The following is a sample job submission:'
    print l_write[0]
    if raw_input('Is this correct? [y,n]: ') == 'y':
        if raw_input('Submit ' + str(len(l_write)) + ' jobs? [y,n]: ') == 'y':
            os.system('chmod 757 batchsub')
            os.system('./batchsub')
