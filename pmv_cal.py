#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/02/21
@brief : PMV计算工具
@author: yutato
"""

import numpy as np

def cal_pmv(ta,tr,vel,rh,clo=0.5,met=1.0,wme=0,basMet=58.15):
    '''
    ta:空气温度(℃)                      
    tr:平均辐射温度(℃)            
    vel:风速(m/s)               
    rh:相对湿度(%)              
    clo:服装热阻(clo)   
    met:新陈代谢率(met)     
    wme:外部做功(met)      
    basMet:基础代谢率(w/m^2)
    '''
    m = met * basMet
    w = wme * basMet
    mw = m - w
    icl = 0.155*clo
    # 计算水蒸气分压力
    pa = rh * 10 * np.exp(16.6536 - (4030.183 / (ta + 235))) 
    # 服装表面积系数fcl
    if (icl <= 0.078):
        fcl = 1 + 1.29*icl
    else:
        fcl = 1.05 + 0.645*icl
    #
    fcic = icl * fcl 
    p2 = fcic * 3.96
    p3 = fcic * 100
    tra = tr + 273
    taa = ta + 273
    p1 = fcic * taa
    p4 = 308.7 - 0.028*mw + p2*(tra/100)**4
    # First guess for surface temperature
    tclA = taa + (35.5-ta) / (3.5 * (6.45 * icl + 0.1))
    xn   = tclA / 100
    xf   = xn
    hcf  = 12.1 * (vel)**0.5
    noi  = 0
    eps  = 0.00015
    # Compute surface temperature of clothing by iterations
    # 迭代计算人体外表面平均温度
    while(noi < 150):
        xf  = (xf+xn)/2
        hcn = 2.38*abs(100*xf-taa)**0.25
        if hcf > hcn:
            hc = hcf
        else:
            hc = hcn
        xn  = (p4+p1*hc-p2*xf**4)/(100+p3*hc)
        noi = noi + 1
        if (noi >1) and (abs(xn-xf)<=eps):
            break
    tcl = 100*xn-273

    # compute pmv
    pm1 = 3.96*fcl*(xn**4-(tra/100)**4)
    pm2 = fcl*hc*(tcl-ta)
    pm3 = 0.303*np.exp(-0.036*m)+0.028
    if mw > basMet:
        pm4 = 0.42*(mw-basMet)
    else:
        pm4 = 0
    pm5 = 3.05*0.001*(5733-6.99*mw-pa)
    pm6 = 1.7*0.00001*m*(5867-pa)+0.0014*m*(34-ta)
    pmv = pm3*(mw-pm5-pm4-pm6-pm1-pm2)

    # compute pdd
    pdd = 100-95*np.exp(-0.03353*pmv**4-0.2179*pmv**2)

    return pmv,pdd

def main():
    
    # 空气温度
    Temp_air = 15
    # 平均辐射温度
    Temp_rad = 15
    # 空气湿度 %
    Humidity = 60
    # 风速
    Velocity = 0.1
    # 新陈代谢率，单位 W/s
    # {'sleep':float(0.7),'stand':float(1.2),'sit':float(1.0)}
    Met_rate = 1.0
    # 服装热阻{'summer'：0.5,'winter':1.0}
    Cloth_ins = 1.0

    pmv,pdd = cal_pmv(Temp_air,Temp_rad,Velocity,Humidity,Cloth_ins,Met_rate)
    
    #print('PMV: ',pmv);print('PDD: ',pdd)
    print('PMV: %2.2f'%(pmv));print('PDD: %2.0f%%'%(pdd))

if __name__ == '__main__':
    main()