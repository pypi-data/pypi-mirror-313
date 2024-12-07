#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   read_edf_of_Philips 
@Time        :   2023/9/21 10:26
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd
from matplotlib import pyplot as plt

from wuji.Reader.EDF.Philips import PhilipsEDFReader
from wuji.Reader.Annotation.Philips import PhilipsAnnotationReader

edf_file_path = '/Users/cxs/Downloads/scored studies/00000818-113072/00000818-113072_2949177.edf'
annotation_file_path = '/Users/cxs/Downloads/scored studies/00000818-113072/00000818-113072.rml'

edf_reader = PhilipsEDFReader(edf_file_path)
annotation_reader = PhilipsAnnotationReader(annotation_file_path)
print(annotation_reader.get_standard_AH_events())
print(edf_reader.signal_labels)
chest = edf_reader.get_signal(ch_name='Effort ABD', tmin=3600, tmax=3660)
abdomen = edf_reader.get_signal(ch_name='Effort THO', tmin=3600, tmax=3660)
ecg = edf_reader.get_signal(ch_name='ECG I', tmin=3600, tmax=3660)
ppg = edf_reader.get_signal(ch_name='Pleth', tmin=3600, tmax=3660)
bcg = edf_reader.get_signal(ch_name='electric_data', tmin=3600, tmax=3660)

fig, axes = plt.subplots(5, 1)
axes[0].plot(chest, label='chest')
axes[1].plot(abdomen, label='abdomen')
axes[2].plot(ecg, label='ecg')
axes[3].plot(ppg, label='ppg')
axes[4].plot(bcg, label='bcg')
plt.show()

AH_events = annotation_reader.get_standard_AH_events()
sleep_stages = annotation_reader.get_standard_sleep_stages()
print(AH_events)
print(sleep_stages)
