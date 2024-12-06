#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   detect_OD_events 
@Time        :   2024/9/13 11:11
@Author      :   Xuesong Chen
@Description :   
"""


from wuji.Reader.EDF.Philips import PhilipsEDFReader
from wuji.algo.Oxygen.detect_oxygen_desaturation import detect_oxygen_desaturation_by_pobm
from wuji.Preprocessor.signal import filter_spo2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # 调用函数detect_oxygen_desaturation_pobm，输入是spo2，1Hz采样率
    edf_path = '/Users/cxs/Downloads/00002657-LEBS20454_4128819.edf'
    edf_reader = PhilipsEDFReader(edf_path)
    spo2_sig = edf_reader.get_signal(ch_name='SpO2', tmin=None)
    spo2_fs = edf_reader.get_sample_frequency(ch_name='SpO2')

    #############################
    #           deploy          #
    #############################
    # 降采样+去掉坏段
    filter_spo2_sig = filter_spo2(spo2_sig, fs=spo2_fs)
    spo2_fs = 1
    # 氧降事件检测
    test_desat1 = detect_oxygen_desaturation_by_pobm(filter_spo2_sig)

    plt.plot(np.round(filter_spo2_sig))
    test_desat1['End'] = test_desat1['Start'] + test_desat1['Duration']
    for index, row in test_desat1.iterrows():
        plt.axvspan(row['Start'], row['End'], facecolor='red', alpha=0.5)
    plt.show()
