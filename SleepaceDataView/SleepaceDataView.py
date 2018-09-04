#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 10:54:35 2018

@author: yutato
"""

from __future__ import division
import sys,os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import matplotlib.pyplot as plt
import numpy as np

# private lib
import data,files

qtCreatorFile = "ui/plt_sleepace.ui" # Enter UI file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # 基本设置信息
        self.settings  = ''
        self.input_dir = ''
        self.file_name = ''
        # 存储数据的变量
        self.raw_data  = []
        self.gain = []
        self.gain_incode = []
        self.offbed_real = []
        self.offbed_his  = []
        # 函数调用
        self.print_input_dir() # 启动时打印默认输入路径下的输入数据
        self.obj_dev_list.currentTextChanged.connect(self.print_input_dir) # 更改设备时，打印相应输入文件路径下的文件

        self.obj_button_plot.clicked.connect(self.click_plotting_button)
        
    def get_dev_name(self):
        return self.obj_dev_list.currentText()
    
    def get_mode_name(self):
        return self.obj_mode_list.currentText()

    def get_sampling_rate(self):
        return self.obj_fs_list.currentText()
        
    def get_alg_version(self):
        return self.obj_alg_list.currentText()

    def get_input_fname(self):
        return self.obj_input_fname.toPlainText()

    def get_file_list(self):
        dev_name = self.get_dev_name()
        if 'LZ300' == dev_name:
            self.input_dir = 'F:/project/data/input_lgbeta/lab/'
            data.inbase    = self.input_dir
            data.outbase   = 'F:/project/data/output_lgbeta/'
        if 'M500/M600' == dev_name:
            self.input_dir = 'F:/project/data/input_chuangdian/'
        if 'Binatone' == dev_name:
            self.input_dir = 'F:/project/data/input_binatone/'
            data.inbase = self.input_dir
        file_list = os.listdir(self.input_dir)
        return file_list

    def get_raw_data(self):
        self.obj_test.append('>> Reading raw data...')
        self.file_name = self.get_input_fname()
        self.raw_data,self.gain = data.read_raw(self.file_name,mode=self.get_mode_name())
        self.obj_test.append('[OK]')

    def get_offbed_data(self):
        self.obj_test.append('>> Reading offbed data...')
        self.file_name   = self.get_input_fname()
        self.offbed_real = data.read_onbed(self.file_name,mode='real')
        self.offbed_his  = data.read_onbed(self.file_name,mode='his')
        self.obj_test.append('[OK]')

    # sample function
    def get_xxx(self):
        self.obj_test.append('>> Reading xxx data...')
        self.file_name = self.get_input_fname()
        #self.xxx = data.read_xxx(self.file_name,mode=self.get_mode_name())
        self.obj_test.append('[OK]')

    def click_plotting_button(self):
        # read settings
        dev_name  = self.get_dev_name()
        mode_name = self.get_mode_name()
        fs        = self.get_sampling_rate()
        alg_ver   = self.get_alg_version() 
        file_name = self.get_input_fname()
        self.settings  = 'device name: ' + dev_name + '\n' + 'mode: ' + mode_name  + '\n' \
                         + 'sampling rate: ' + fs + '\n' + 'algorithm: ' + alg_ver + '\n' \
                         + 'file name: ' + file_name
        self.obj_test.setText(self.settings) 

        # read data
        self.get_raw_data()
        self.get_offbed_data()
        
        # plot 
        #if self.checkBox_7.isChecked() :
        self.plt_all()
        
    def print_input_dir(self):
        file_list = self.get_file_list()
        self.obj_fname_browser.clear()
        for item in file_list:
            self.obj_fname_browser.append(item)

    def plt_all(self):
        plt.figure()
        plt.subplot(311)
        plt.plot(np.array(self.raw_data)-32768)
        plt.subplot(312)
        plt.plot(self.offbed_his)
        plt.subplot(313)
        plt.plot(self.offbed_real)
        plt.show()

    def plt_offbed(self):
        pass
        
    def runexe(self):
        #cmdline = exefile + ' ' + input_filename + ' ' + output_dir
        #os.system(cmdline)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
    