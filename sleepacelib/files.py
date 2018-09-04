#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:57:09 2018
@brief : 跟文件处理相关的函数模块.
@author: yutato
"""
import os,time
import pandas as pd
import numpy  as np
from datetime import datetime
HEADER = ['Time','SaO2','HeartRate']
DATEFORMAT = '%m/%d/%Y %H:%M:%S'
# function: ls
def ls(path):


    
    print('-'*10)
    dirlist = os.listdir(path)
    print('Total %d files(dirs):'%len(dirlist))

    i = 0
    for i in range(len(dirlist)): 
        '''i = i+1
        if 0==(i%3):
            print('\t')
        else:
            print('%-45s'%item,end="")'''
        #print(dirlist[i])
        if os.path.isfile:
            print('%2d'%(i+1),'<file>',dirlist[i])

    print('-'*10)
# end: ls

# function: get_filename
def get_filename(workpath,postfix,fix=True):
    
    fname = []
    flist = os.listdir(workpath)

    for i in flist:
        if postfix == os.path.splitext(i)[-1]:
            if fix:
                fname.append(i)
            else:
                prename = os.path.splitext(i)[0]
                fname.append(prename)
    return fname
# end: get_filename

# funcion: get_prefix
def get_prefix(filename):
    return os.path.splitext(filename)[0]
# end: get_prefix

# function: get_date_fromfilename
def get_date_fromfilename(filename):
    #filename = '2018-03-14-56天-2022-沈.csv'
    namepice = filename.split('-')

    year,month,day, = namepice[0],namepice[1],namepice[2]
    hour,minute,second = namepice[4][:2],namepice[4][-2:],'01'

    dtime =  month+'/'+day+'/'+year+' '+hour+':'+minute+':'+second
    rlst = datetime.strptime(dtime,'%m/%d/%Y %H:%M:%S')
    return rlst
# end: get_date_fromfilename

# function: get_date_fromfilename
def get_date_fromfilename1(filename):
	
	#filename  = '14310_1526828700_0_50Hz.dat'
	tstamp = filename.split('_')[1]
	tlocal = time.localtime(int(tstamp))
	tstring = time.strftime('%m/%d/%Y %H:%M:%S',tlocal)
	rslt = datetime.strptime(tstring,'%m/%d/%Y %H:%M:%S')
	return rslt
# end: get_date_fromfilename

# function: get_date_fromtimestamp
def get_date_fromtimestamp(tstamp):
    #return datetime.utcfromtimestamp(tstamp)
    rlst = datetime.fromtimestamp(tstamp)
    return rlst
# end: get_data_fromtimestamp

# function: get_timestamp
def get_timestamp(dtime):
    #stime = time.strptime(dtime,DATEFORMAT)
    #return int(time.mktime(stime))
    return time.mktime(dtime.timetuple())
# end: get_timestamp

def get_time_fromfilname(filename,datalen,freq=100.0):
    
    idelta = 1.0/freq

    starttime  = get_date_fromfilename(filename)
    startstamp = get_timestamp(starttime)
    timeserie  = [startstamp+i*idelta for i in range(datalen)]
    timeaxis   = [get_date_fromtimestamp(i) for i in timeserie]

    return timeaxis

def get_date_frompd(pddata):
    
    dtime = pddata['Time']
    rlst  = [datetime.strptime(i.strip(),'%m/%d/%Y %H:%M:%S') for i in dtime]

    return rlst

def get_date_fromfilestat(filename):
     fstat = os.stat(filename)
     mtime = fstat.st_mtime
     return datetime.fromtimestamp(mtime)