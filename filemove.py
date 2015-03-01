import os
import subprocess

new_dir = 'DFTB'

fo = open('filemove.csv')
filedata = fo.readlines()
fo.close

print filedata
logfilenames = filedata[0].split('\r')
print logfilenames

print 'i got here'    

gjffilenames=[]    
for i in range(len(logfilenames)):
    gjffilenames.append(logfilenames[i].split('.')[0] + '.gjf')
    print gjffilenames[i]
    print logfilenames[i]
    

test = os.system('pwd > f.txt')
f = open('f.txt')
cd = f.readlines()[0].split('\n')[0]
f.close
os.system('rm f.txt')

print cd

for i in range(len(gjffilenames)):        os.system('cp ' + '/orc_lfs/' + cd  + gjffilenames[i] + ' ' + cd + '/orc_lfs/'+new_dir+'/')    os.system('cp ' + '/orc_lfs/' + cd  + logfilenames[i] + ' ' + cd + '/orc_lfs/'+new_dir+'/')
