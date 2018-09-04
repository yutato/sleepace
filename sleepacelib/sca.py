#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:15:09 2018
@filename: sleep cycle analysis (sca.py)
@brief   : 读取睡眠分析的原始、结果和各类中间数据的模块.
@author  : yutato
"""
import struct
import numpy as np
from scipy import signal as sig

inbase  = 'F:/project/data/input_app/' 
outbase = 'F:/project/data/output_app/'

def read_featrue(filename):
    
    brate,hrate,statue,statvalue = [],[],[],[]
    fname = inbase + filename
    f = open(fname,'rb')
    dtmp  = f.read()
    #print(len(dtmp))
    dbyte = _byte2int(dtmp,mode='u8')

    i = 0 
    while(i<len(dbyte)):
        brate.append(dbyte[i])
        hrate.append(dbyte[i+1])
        statue.append(dbyte[i+2]&0x07)  #[0:2,3:7],低3位为状态，高5位留作它用。
        statvalue.append(dbyte[i+3])
        i = i + 4
    
    rslt = {'Brate':brate,'Hrate':hrate,'Statue':statue,'StatValue':statvalue}

    return rslt 
# end:

def read_sleepstage(filename):
    
    fname = outbase + 'SleepStage/' + filename
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = _byte2int(dtmp,mode='u8')
    return rslt
# end:

def read_sleepevent(filename):
    fname = outbase + 'SleepEvent/' + filename
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = _byte2int(dtmp,mode='u16')
    return rslt
# end:

def read_sleepcurve(filename):
    fname = outbase + 'SleepCurve/' + filename
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = _byte2float(dtmp,mode='float')
    return rslt
# end:

def read_sleepdata(filename):
    fname = outbase + 'Analysis/' + filename
    f = open(fname,'rb')
    dtmp = f.read()
    dtmp = bytearray(dtmp)
    mean_brate = dtmp[0]
    mean_hrate = dtmp[1]
    min_of_asleep = dtmp[2] | dtmp[3]<<8
    min_of_awake  = dtmp[4] | dtmp[5]<<8
    min_of_offbed = dtmp[6] | dtmp[7]<<8
    min_of_disc   = dtmp[8] | dtmp[9]<<8

    return mean_brate,mean_hrate,min_of_asleep,min_of_awake,min_of_offbed,min_of_disc

def read_sleepbpause(filename):
    fname = outbase + 'Bpause/' + filename
    
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = _byte2int(dtmp,mode='u8')
    return rslt


# function: byte2int
def _byte2int(data,mode='u16'):

    dbyte = bytearray(data)
    darray  = []
    
    i = 0
    while( i < len(dbyte)):
        
        if ('u8' == mode):
            darray.append(dbyte[i])
            i = i +1
        elif ('u16' == mode):
            darray.append(dbyte[i] | dbyte[i+1]<<8)
            i = i + 2
    
    return darray
# end: byte2int

# function: byte2float
def _byte2float(data,mode='float'):
    
    darray = []

    i = 0
    if 'float' == mode:
        while(i < len(data)):
            fx = struct.unpack('f',data[i:i+4])
            darray.append(fx)
            i = i + 4
    elif 'double' == mode:
        while(i < len(data)):
            dx = struct.unpack('d',data[i:i+8])
            darray.append(dx)
            i = i + 8

    return darray
# end: byte2float


