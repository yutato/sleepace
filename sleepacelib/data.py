#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:57:09 2018
@brief : 读取原始、结果和各类中间数据的模块.
@author: yutato
"""
import struct
import numpy as np
from scipy import signal as sig

inbase  = 'F:/project/data/input_xg/' 
outbase = 'F:/project/data/output_xg/'

#---------- I.原始数据相关函数 ----------#
# function: read_raw
def read_raw(fname,mode='server'):
    """
    返回原始信号和增益（编码）.
    参数
    ----
        mode = {'server'（默认）, 'app'}.
        'server'，表示原始信号的存储格式为 3 字节，前两个字节存储的是信号（低位优先），第三个字节存储的是增益.
        'app'，表示原始信号的存储格式为 2 字节，第一个字节存储信号的高八位，第二个字节的前 4 位是信号的低四位，后 4 位是增益.
    返回值
    ------
        bcg : 原始信号 
        gain: 增益（未解码）
    """
    print('read raw signal and gain.')
    bcg,gain = [],[]
    
    fname = inbase + fname
    f = open(fname,'rb')
    dtmp  = f.read()
    dbyte = bytearray(dtmp)
    
    i = 0
    while(i < len(dbyte)):
        if 'server' == mode:
            bcg.append(dbyte[i] | dbyte[i+1]<<8)
            gain.append(dbyte[i+2])
            i = i + 3
        elif 'app' == mode:
            bcg.append((dbyte[i]) | (dbyte[i+1]<<8))
            gain.append(dbyte[i] & 0x0F)
            i = i + 2
       
    return bcg,gain
# end: read_raw

# function: read_rawsignal
def read_rawsignal(fname,mode='server',sampling_rate=100):
    """
    返回原始信号和增益（编码）.
    参数
    ----
        mode = {'server'（默认）, 'app'}.
            'server'，表示原始信号的存储格式为 3 字节，前两个字节存储的是信号（低位优先），第三个字节存储的是增益.
            'app'，表示原始信号的存储格式为 2 字节，第一个字节存储信号的高八位，第二个字节的前 4 位是信号的低四位，后 4 位是增益.
        sampling_rate = {50, 100(默认)}.																																																																																																																																			
    返回值
    ------
        bcg : 原始信号 
        gain: 增益（未解码）
    """		
    print('read raw signal and gain.')																																																																																																																																																																																																																																																																											
    bcg,gain = [],[]
    
    fname = inbase + fname
    f = open(fname,'rb')
    dtmp  = f.read()
    dbyte = bytearray(dtmp)

    i = 0
    if 'server' == mode:
        while(i < len(dbyte)):
            if 100 == sampling_rate:
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                gain.append(dbyte[i+2])
            elif 50 == sampling_rate:
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                gain.append(dbyte[i+2])
                gain.append(dbyte[i+2])
            i = i + 3
    elif 'app' == mode:
        while(i < len(dbyte)):
            if 100 == sampling_rate:
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                gain.append(dbyte[i] & 0x0F)
            elif 50 == sampling_rate:
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                bcg.append(dbyte[i] | dbyte[i+1]<<8)
                gain.append(dbyte[i] & 0x0F)
                gain.append(dbyte[i] & 0x0F)
            i = i + 2
    return bcg,gain
# end: read_rawsignal

# function: read_rawsignal
def read_rawtwo(fname,mode='server'):
    """
    返回原始信号(bcg和振动)和增益（编码）.																																																																																																																																			
    返回值
    ------
        bcg,gain_bcg,dcs,gain_dcs : BCG信号和增益,DC信号和增益. 
    """		
    print('read raw signal and gain.')
    siganl_a,gain_a = [],[]
    signal_b,gain_b = [],[]

    fname = inbase + fname
    f = open(fname,'rb')
    dtmp  = f.read()
    dbyte = bytearray(dtmp)

    i = 0
    # 100HZ
    if 'app' == mode:
        while(i < len(dbyte)):
            siganl_a.append(dbyte[i] | dbyte[i+1]<<8)
            siganl_a.append(dbyte[i] | dbyte[i+1]<<8)
            gain_a.append(dbyte[i+1] & 0x0F)
            gain_a.append(dbyte[i+1] & 0x0F)
            signal_b.append((dbyte[i+2] | dbyte[i+3]<<8))
            signal_b.append((dbyte[i+2] | dbyte[i+3]<<8))
            gain_b.append(dbyte[i+3] & 0x0F)
            gain_b.append(dbyte[i+3] & 0x0F)
            i = i + 4
    elif 'server' == mode:
        while(i < len(dbyte)):
            siganl_a.append(dbyte[i] | dbyte[i+1]<<8)
            gain_a.append(dbyte[i+2] & 0x0F)
            i = i + 3

    return siganl_a,gain_a,signal_b,gain_b
# end: read_rawsignal

def read_bcg_and_accel(fname):
    '''
    [] -> byte, H -> Hight Byte, L -> Low Byte, gain -> bcg gain;
    [gz_H][gz_L][gy_H][gy_L][gx_H][gx_L][bcg_L:gain][bcg_H]
    14 bit resolution,full scale = ±4g
    '''
    bcg,gain = [],[]
    gx,gy,gz = [],[],[]

    fname = inbase + fname
    f = open(fname,'rb')
    dtmp  = f.read()
    dbyte = bytearray(dtmp)

    i = 0
    while(i<len(dbyte)):
        gz.append((dbyte[i+0] | (dbyte[i+1]<<8))&0x0FFF)
        gy.append((dbyte[i+2] | (dbyte[i+3]<<8))&0x0FFF)
        gx.append((dbyte[i+4] | (dbyte[i+5]<<8))&0x0FFF)
        bcg.append(dbyte[i+6]| dbyte[i+7]<<8)
        gain.append(dbyte[i+6]   & 0x0F)
        i = i + 8
    
    return bcg,gain,gx,gy,gz

def read_filty(fname):
    fname = outbase + 'Filt_y/' + fname
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = byte2float(dtmp,mode='float')

    return rslt

def read_zetay(fname):
    fname = outbase + 'Zeta_y/' + fname
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = byte2int(dtmp,mode='u8')

    return rslt

#---------- II.在/离床相关函数 ----------#
# function: read_onbed
def read_onbed(fname,mode='real'):
    """
    返回（实时、历史）在/离床状态.
    参数
    ----
        mode = {'real'：实时在离床；'his'：历史在离床}.
    返回值
    -----
        rslt = {0：离床；1：在床}.
    """
    if 'real' == mode:
        print('read onbed satate(real).')
        fname = outbase + 'Result_FlagReal/' + fname
    elif 'his' == mode:
        print('read onbed satate(his).')
        fname = outbase + 'Result_FlagHis/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')

    return rslt
# end: read_onbed

# function: read_onbedwave
def read_onbedwave(fname):
    """
    返回滤波后的在离床信号.
    """
    print('read onbed wave(filted).')
    fname = outbase + 'Result_filtLeave/' + fname
    f = open(fname,'rb')
    dtmp = f.read()

    rslt = byte2float(dtmp,mode='float')

    return rslt
# end: read_onbedwave

# function: read_onbedthreshold
def read_onbedthreshold(fname):
    """
    返回离床阈值.
    """
    print('read onbed threshold.')
    thupper,thlower = [],[]
    fname = outbase + 'Result_LeaveThr_real/' + fname
    
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    
    i = 0
    while(i<len(rslt)):
        x = int(rslt[i])
        thupper.append(x/2+32768)
        thlower.append(-x/2+32768)
        i = i+1

    return thupper,thlower
# end: read_onbedthreshold

# function: read_onbedvpp
def read_onbedvpp(fname,mode='normal'):
    """
    返回在/离床判断的峰-谷值之差(20s均值).
    参数
    ----
        mode = {'normal','mean'}.
    """
    if 'normal' == mode:
        fname = outbase + 'Result_normalVpp/' + fname
    elif 'mean' == mode:
        fname = outbase + 'Result_normalVpp_mean/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')

    return rslt
# end: read_onbedvpp

# function: read_onbedflag
def read_onbedflag(fname,mode='normal'):
    """
    返回在离床判断时的常态/瞬态标记.
    """
    if 'normal' == mode:
        fname = outbase + 'Result_flagNormal/' + fname
    elif 'tran' == mode:
        fname = outbase + 'Result_flagTran/' +fname
    
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')

    return rslt
# end: read_onbedflag

# function: read_onbedtrigger
def read_onbedtrigger(fname,mode='real'):
    """
    返回离床状态转在床状态（实时、历史）标记.
    """
    if 'real' == mode:
        fname = outbase + 'Result_leftBedFlagAct_real/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_leftBedFlagAct_his/' + fname
    
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')

    return rslt
# end: read_onbedtrigger

# function: read_st_energy
def read_st_energy(fname):
    
    fname1 = outbase + 'Result_energy/' + fname
    fname2 = outbase + 'Result_energy_th/' + fname

    f1 = open(fname1,'rb')
    dtmp1 = f1.read()
    energy = byte2float(dtmp1,mode='double')

    f2 = open(fname2,'rb')
    dtmp2 = f2.read()
    energy_th = byte2float(dtmp2,mode='double')

    return energy,energy_th
# end: read_st_energy

def read_th_of_vpp(fname):
    fname = outbase + 'Result_LeaveThr_real/' + fname
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    return rslt

def read_vpp(fname):
    fname = outbase + 'Tmp_vpp/' + fname
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    return rslt

def read_times(fname):
    fname = outbase + 'Tmp_times/' + fname
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    return rslt
    

#---------- III.信号状态相关函数 ----------#
# function: read_bcgstate
def read_bcgstate(fname):
    """
    返回bcg信号的状态.
    返回值
    -----
        rslt = {0:正常, 2:干扰, 3:体动, 4:翻身}.
    """
    print('read bcg siganl states.')
    fname = outbase + 'Result_State/' + fname
    
    f = open(fname,'rb')
    dtemp = f.read()
    rslt = byte2int(dtemp,mode='u8')
    
    return rslt
# end: read_bcgstate

# function: read_gain
def read_gain(fname):
    """
    返回解码增益.
    """
    print('read gain(decode).')
    fname = outbase + 'Result_Gain/' + fname
    
    f = open(fname,'rb')
    dtemp = f.read()
    rslt = byte2int(dtemp,mode='u8')
    
    return rslt
# end: read_gain
    
# function:
def read_(fname):
    """
    """
    pass
# end:

#---------- IV.心率相关函数 ----------#
# function: read_hwave
def read_hwave(fname,mode='result'):
    """
    返回（滤波、平滑、包络）心跳信号.
    参数
    ----
        mode = {'filt'：第一次滤波后的心跳信号；'smooth'：平滑后的心跳信号；'result'：心跳包络信号}.
    """
    print('read heart wave.')
    if 'filt' == mode: 
        fname = outbase + 'Result_filtHB/' + fname
    elif 'smooth' == mode:   
        fname = outbase + 'Result_smoothHB/' + fname
    elif 'result' == mode:   
        fname = outbase + 'Result_HeartWave/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    
    return rslt
# end: read_hwave

# function: read_hpeaks
def read_hpeaks(fname,mode='real'):
    """
    返回心跳包络信号的（实时、历史）峰值.
    """
    if 'real' == mode:    
        fname = outbase + 'Result_HpeakReal/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_Hpeakhis/' + fname
        
    f = open(fname,'rb')
    dtmp = f.read() 
    rslt = byte2int(dtmp,mode='u16')
   
    return rslt
# end: read_hpeaks

# function: read_hrate
def read_hrate(fname,mode='real'):
    """
    返回（实时、历史）心率值.
    """
    if 'real' == mode:    
        fname = outbase + 'Result_HrReal/' + fname
    if 'his' == mode:
        fname = outbase + 'Result_HrHis/' + fname
        
    f = open(fname,'rb')
    dtmp = f.read() 
    drslt = byte2int(dtmp,mode='u16')
   
    return drslt
# end: read_hrate

# function: read_hthreshold
def read_hthreshold(fname,mode='real'):
    """
    返回心率峰值检测的（实时、历史）阈值.
    """
    if 'real' == mode:
        fname = outbase + 'Result_HrThr_real/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_HrThr_hist/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')

    return rslt
# end: read_hthreshold

# function: read_hinterval
def read_hinterval(fname,mode='real'):
    """
    返回心率峰值检测的（实时、历史）间隔值.
    """
    if 'real' == mode:
        fname = outbase + 'Result_HrInter_real/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_HrInter_hist/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')

    return rslt
# end: read_hinterval

# function: read_meanJJ
def read_meanJJ(fname,mode='real'):
    """
    返回心率峰值检测的JJ峰间间隔均值.
    """

    if 'real' == mode:
        fname = outbase + 'Result_Hrmeaninter_real/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_Hrmeaninter_hist/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')

    return rslt
# end: read_meanJJ

#---------- V.呼吸率相关函数 ----------#
# function: read_brate
def read_brate(fname,mode='real'):
    """
    返回（实时、历史）呼吸率值.
    参数
    ----
        mode = {'real'：实时呼吸率值；'his'：历史呼吸率值}.
    """
    if 'real' == mode:    
        fname = outbase + 'Result_BrReal/' + fname
    if 'his' == mode:
        fname = outbase + 'Result_BrHis/' + fname
        
    f = open(fname,'rb')
    dtmp = f.read() 
    rslt = byte2int(dtmp,mode='u16')
   
    return rslt
# end: read_brate

# function: read_bwave
def read_bwave(fname,mode='result'):
    """
    返回呼吸（滤波、包络）信号.
    参数
    ----
        mode = {'result'：呼吸包络；'filt'：滤波后的呼吸信号}.
    """
    if 'result' == mode:
        fname = outbase + 'Result_RespWave/' + fname
    elif 'filt' == mode:
        fname = outbase + 'Result_filtResp/' + fname

    f = open(fname,'rb')
    dtemp = f.read()
    drslt = byte2int(dtemp,mode='u16')
    
    return drslt
# end: read_bwave

# function: read_bpeaks
def read_bpeaks(fname,mode='real'):
    """
    返回呼吸包络的峰值.
    参数
    ----
        mode = {'real'：实时峰值；'his'：历史峰值}.
    """
    if 'real' == mode:
        fname = outbase + 'Result_RpeakReal/' + fname    
    elif 'his' == mode:
        fname = outbase + 'Result_Rpeakhis/' + fname

    f = open(fname,'rb')
    dtemp = f.read()
    drslt = byte2int(dtemp,mode='u16')

    return drslt
# end: read_peaks

# function: read_bthreshold
def read_bthreshold(fname,mode='real'):
    
    if 'real' == mode:
        fname = outbase + 'Result_RespThrIntr_real/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_RespThrIntr_hist/' + fname

    f = open(fname,'rb')
    dtmp  = f.read()
    drslt = byte2int(dtmp,mode='u16')

    return drslt
# end: read_bthreshold

#---------- VI.呼吸暂停相关函数 ----------#
# function: read_apnea
def read_bflag(fname,mode='real'):  
    """
    返回呼吸状态值.
    参数
    ----
        mode = {'real'：实时呼吸状态；'his'：历史呼吸状态}.
    返回值
    -----
        rslt = {2：呼吸正常；3：呼吸暂停}
    """
    if 'real' == mode:
        fname = outbase + 'Result_FlagRespReal/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_FlagRespHis/' + fname
        
    f = open(fname,'rb')
    dtmp = f.read()
    drslt = byte2int(dtmp,mode='u8') 

    return drslt
# end: read_apnea

# function: read_apneawave
def read_apneawave(fname):
    """
	返回滤波后的呼吸暂停信号
    """
    fname = outbase + 'Result_filtRespState/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u16')
    

    return rslt
# end: read_apneawave

#---------- VII.固件输出数据相关函数（Zx-1.1.1-4） ----------#
# function: read_oneminrate
def read_oneminrate(fname,mode='heart'):
    """
    返回心率、呼吸率，按分钟算（即每分钟对应一个值）.
    参数 
    ----
        mode = {'heart'：返回心率；'resp'：返回呼吸率}.
    """
    if 'heart' == mode:
        fname = outbase + 'Result_HR_1min/' + fname
    elif 'resp' == mode:
        fname = outbase + 'Result_BR_1min/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')

    return rslt
# end: read_oneminrate

# function: read_oneminflag
def read_oneminflag(fname):
    """
    返回每分钟的刷新标记.
    返回值
    -----
        rslt = {0：数据未准备；1：数据准备；2：数据保持}
    """

    fname = outbase + 'Result_Flag_1min/' + fname

    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')
    
    return rslt
# end: read_oneminflag

# function: read_oneminstate
def read_oneminstate(fname):
    """
    返回每分钟的状态，和状态值.
    返回值 
    -----
        state = {0：正常；1：初始化；2：呼吸暂停；3：心跳暂停；4：体动；5：离床；6：翻身}
        svalue，每分钟内各状态出现的次数.
    """
    fname1 = outbase + 'Result_compositState_1min/' + fname
    fname2 = outbase + 'Result_compositStateValue_1min/' + fname
    
    f1 = open(fname1,'rb')
    dtmp1 = f1.read()
    state = byte2int(dtmp1,mode='u8')

    f2 = open(fname2,'rb')
    dtmp2 = f2.read()
    svalue = byte2int(dtmp2,mode='u8')

    return state,svalue 
# end: read_oneminstate

# function: 
def read_stateHz(fname,mode='real'):
    """
    返回100Hz的状态值.
    返回值
    -----
        rslt = {0：正常；1：初始化；2：呼吸暂停；3：心跳暂停；4：体动；5：离床；6：翻身}.
    """
    if 'real' == mode:
        fname = outbase + 'Result_compositStateReal/' + fname
    elif 'his' == mode:
        fname = outbase + 'Result_compositStateHis/' + fname
    
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')

    return rslt
# end:

def read_sleepstage(fname):
    fname = outbase + 'Result_SleepStage/' + fname
    f = open(fname,'rb')
    dtmp = f.read()
    rslt = byte2int(dtmp,mode='u8')
    return rslt

#---------- VIII.其他函数 ----------#
def get_maxandmin(data):
    
    dlist = list(data)
    dmin  = 200
    for i in dlist:
        if ((i > 0)and(i <= dmin)):
            dmin = i

    dmax = max(dlist)
    imin, imax = dlist.index(dmin), dlist.index(dmax)

    return imin,dmin,imax,dmax
# function: get_peaks
def get_peaks(data,widths=(8,)):
    '''
    输入一个1-D的数据信号，返回该信号的峰值，和峰值所在位置.
    parameters：
        data  : 1-D array in which to find the peaks.
        widths: 1-D array of widths to use for calculating the CWT matrix.
    returns：
        pvalus: Peaks value of the sig were found.
        pindex: Indices of the locations in the vector where peaks were found.
    '''
    #pvalue = []
    ppeaks = []
    
    pindex = sig.find_peaks_cwt(data,widths)
    '''
    for i in pindex:
        pvalue.append(data[i])
    '''
    for i in range(len(data)):
        if i in pindex:
            ppeaks.append(data[i])
        else:
            ppeaks.append(0)

    return ppeaks,pindex
# end: get_peaks

def get_fftpack(data):
    from scipy import fftpack

    rslt = fftpack.hilbert(data)

    return rslt

# function: filt_kalman
def filt_kalman(data,q=1e-5,r=2e-4):
    drslt = []
    P = 1.0
    Q = q
    R = r
    K = 0.0
    X = 100.0
    for i in range(len(data)):
        K = P/(P+R)
        X = X + K*(data[i]-X)
        P = (1-K)*P + Q
        drslt.append(round(X))
    return drslt
# end: filt_kalman

#---------- VIIII.内部函数 ----------#
# function: byte2int
def byte2int(data,mode='u16'):

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
def byte2float(data,mode='float'):
    
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
