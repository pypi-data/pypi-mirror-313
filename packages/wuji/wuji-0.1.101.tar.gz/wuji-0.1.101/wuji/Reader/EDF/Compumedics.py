# _*_ coding: utf-8 _*_
# @Author : ZYP
# @Time : 2024/11/1 16:03
#
import numpy as np
import pyedflib
from datetime import datetime
import pandas as pd
import itertools
from cpmreader.cpm import read_psg_compumedics, PSGcompumedics

def export_edf_from_raw(folder):
    pg = PSGcompumedics(folder)
    dtcdata = pg.raw_data(include='all')
    hypnogram = pg.hypnogram()
    events = pg.events()
    start_time = pg.start_date()
    file_name = f'{folder}/output_data.edf'
    num_channels = 26
    with pyedflib.EdfWriter(file_name, num_channels, file_type=pyedflib.FILETYPE_EDFPLUS) as f:
        # 设置起始时间
        f.setStartdatetime(start_time)
        signal_headers = []
        raw_data = []
        labels = []
        f.update_header()
        for i, (channel_key, channel_data) in enumerate(itertools.islice(dtcdata.items(), 26)):
            # 提取通道信息
            label = channel_key
            dimension = channel_data.get('UnitOfMeasure', '')
            sample_rate = int(channel_data['Rate'])
            physical_max = float(channel_data.get('Sensitivity', 1))
            physical_min = -float(channel_data.get('Sensitivity', 1))
            digital_max = 32767
            digital_min = -32768

            # 构建通道信息字典
            channel_info = {
                'label': label,
                'dimension': dimension,
                'sample_rate': sample_rate,
                'sample_frequency': sample_rate,
                'physical_max': physical_max,
                'physical_min': physical_min,
                'digital_max': digital_max,
                'digital_min': digital_min,
                'prefilter': '',
                'transducer': ''
            }
            signal_headers.append(channel_info)
            labels.append(label)
            # 设置信号头信息
            f.setSignalHeader(i, channel_info)
            f.setLabel(i, label)
            f.setSamplefrequency(i, sample_rate)
            f.setPhysicalMaximum(i, physical_max)
            f.setPhysicalMinimum(i, physical_min)
            f.setDigitalMaximum(i, digital_max)
            f.setDigitalMinimum(i, digital_min)
            # 写入数据
            data_array = channel_data['data']
            raw_data.append(channel_data['data'])
        f.setSignalHeaders(signal_headers)
        f.writeSamples(raw_data)

    print("Data has been successfully written to", file_name)


if __name__ == '__main__':
    folder = '/Users/cxs/Downloads/test_edf/'
    export_edf_from_raw(folder)
    exported_edf_fp = f'{folder}/output_data.edf'
    baseline_fp = '/Users/cxs/Downloads/EXPORT.edf'
    from wuji.Reader.EDF.Base import Base, EDFHeaderParser
    exported_edf_header = EDFHeaderParser(exported_edf_fp)
    baseline_edf_header = EDFHeaderParser(baseline_fp)
    print(exported_edf_header)
    print(baseline_edf_header)
    # exported_reader = Base(exported_edf_fp)
    baseline_reader = Base(baseline_fp)
    # spo2 = baseline_reader.get_signal(ch_name='Ox Status')
    # np.savetxt('ox_status_fs16_edf.txt', spo2, fmt='%d')
    print()

