############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       01/01/2015       ##
##scnt_timestamp_refresh.py#
##         v1.4           ##
############################
"""
Created on Thu Feb 26 13:27:32 2015

@author: lukemelo

Run this program to update the timestamp of eall files in the current directory
"""
import os

os.system('ls -p | grep -v / > filedir.csv')
    
fo = open('filedir.csv', 'r')
filenames = fo.readlines()
print filenames
fo.close()
print 'Filelist compiled in current directory.'
print 'Processing files in current directory...'


for i in range(len(filenames)):
    cur_file = filenames[i].split('\n')[0]
    fr = open(cur_file,'r')
    file_contents = fr.readlines()
    fr.close()
    
    fw = open(cur_file,'w+')
    fw.writelines(file_contents)
    fw.close()