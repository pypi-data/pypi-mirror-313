# !/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Base 
@Time        :   2023/8/18 14:34
@Author      :   Xuesong Chen
@Description :   
"""
import datetime
import re

import matplotlib.pyplot as plt
import numpy as np
from pyedflib.edfreader import EdfReader
import json
from collections import OrderedDict


def _assign_signal_types(signal_labels):
    signal_type = []
    for idx, sig in enumerate(signal_labels):
        if re.search('CO2', sig, re.IGNORECASE):
            signal_type.append('unk')
        elif re.search('E[CK]G', sig, re.IGNORECASE):
            signal_type.append('ecg')
        elif re.search('S[pa]O2', sig, re.IGNORECASE):
            signal_type.append('spo2')
        elif re.search('ABD', sig, re.IGNORECASE):
            signal_type.append('abd')
        elif re.search('CHEST|THO', sig, re.IGNORECASE):
            signal_type.append('chest')
        elif re.search('EEG|C3-M2|C4-M1|F3-M2|F4-M1|O1-M2|O2-M1|C3|C4|F3|F4|O1|O2', sig, re.IGNORECASE):
            if re.search('DIF[34][+-]', sig, re.IGNORECASE):
                signal_type.append('unk')
            else:
                signal_type.append('eeg')
        elif re.search('EMG', sig, re.IGNORECASE):
            signal_type.append('emg')
        elif re.search('EOG', sig, re.IGNORECASE):
            signal_type.append('eog')
        elif re.search('Snore', sig, re.IGNORECASE):
            signal_type.append('snore')
        elif re.search('position', sig, re.IGNORECASE):
            signal_type.append('position')
        elif re.search('AirFlow', sig, re.IGNORECASE):
            signal_type.append('nasal_thermometer')
        elif re.search('CFLOW|Pressure', sig, re.IGNORECASE):
            signal_type.append('nasal_pressure')
        elif re.search('Flow|NEW AIR', sig, re.IGNORECASE):
            signal_type.append('flow')
        elif re.search('Numeric Aux', sig, re.IGNORECASE):
            signal_type.append('trigger')
        elif re.search('Pleth', sig, re.IGNORECASE):
            signal_type.append('ppg')
        else:
            signal_type.append('unk')
    signal_type = np.array(signal_type, dtype='U20')
    return signal_type


class EDFHeaderParser:
    def __init__(self, filename):
        self.filename = filename
        self.edf_header = OrderedDict()
        self.signal_header = None
        self.sigal_labels = None
        self._debug_parse_header()

    def _debug_parse_header(self):
        with open(self.filename, 'rb') as f:
            f.seek(0)
            self.edf_header['version'] = f.read(8).decode().strip()
            self.edf_header['patient_id'] = f.read(80).decode().strip()
            self.edf_header['recording_id'] = f.read(80).decode().strip()
            self.edf_header['startdate'] = f.read(8).decode().strip()
            self.edf_header['starttime'] = f.read(8).decode().strip()
            self.edf_header['header_n_bytes'] = f.read(8).decode().strip()
            self.edf_header['reserved'] = f.read(44).decode().strip()
            self.edf_header['n_records'] = f.read(8).decode().strip()
            self.edf_header['record_duration'] = f.read(8).decode().strip()
            self.edf_header['n_signals'] = f.read(4).decode().strip()
            nsigs = int(self.edf_header['n_signals'])
            label = [f.read(16).decode().strip() for i in range(nsigs)]
            transducer = [f.read(80).decode().strip() for i in range(nsigs)]
            dimension = [f.read(8).decode().strip() for i in range(nsigs)]
            physical_min = [float(f.read(8).decode().strip()) for i in range(nsigs)]
            physical_max = [float(f.read(8).decode().strip()) for i in range(nsigs)]
            digital_min = [int(f.read(8).decode().strip()) for i in range(nsigs)]
            digital_max = [int(f.read(8).decode().strip()) for i in range(nsigs)]
            prefilter = [f.read(80).decode().strip() for i in range(nsigs)]
            sample_rate = [f.read(8).decode().strip() for i in range(nsigs)]
            reserved = [f.read(32).decode().strip() for i in range(nsigs)]
        _ = zip(label, transducer, dimension, physical_min, physical_max, digital_min, digital_max, prefilter,
                sample_rate, reserved)
        values = locals().copy()
        fields = ['label', 'transducer', 'dimension', 'physical_min', 'physical_max', 'digital_min', 'digital_max',
                  'prefilter', 'sample_rate', 'reserved']
        self.signal_header = [{field: values[field][i] for field in fields} for i in range(nsigs)]

    def get_signal_labels(self):
        if self.sigal_labels is not None:
            return self.sigal_labels
        self.sigal_labels = np.array([sig['label'] for sig in self.signal_header])
        return self.sigal_labels

    def get_duration(self):
        return float(self.edf_header['n_records'])

    def get_recording_start_time(self):
        datetime_format = '%d.%m.%y %H.%M.%S'
        time_info = datetime.datetime.strptime(self.edf_header['startdate'] + ' ' + self.edf_header['starttime'],
                                               datetime_format)
        return time_info


class Base:
    def __init__(self, file_path):
        self._parse_file(file_path)

    def _parse_file(self, file_path):
        self.reader = EdfReader(file_path)
        self.signal_labels = np.array(self.reader.getSignalLabels())
        self.duration = self.reader.getFileDuration()
        self._assign_signal_types()

    def close(self):
        if self.reader:
            self.reader.close()
            self.reader = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _assign_signal_types(self):
        self.signal_type = _assign_signal_types(self.signal_labels)

    def get_start_recording_time(self):
        return self.reader.getStartdatetime()

    def get_number_of_signals(self, type='ecg'):
        return np.sum(self.signal_type == type)

    def get_channel_name(self, type='ecg', order=None):
        if order is None:
            return self.signal_labels[self.signal_type == type]
        else:
            return self.signal_labels[self.signal_type == type][order]

    def _get_eeg_ecg_in_mV(self, dimension, skip_dim=False):
        if skip_dim:
            return 1
        assert dimension in ['uV', 'mV', 'V'], f'Unknown dimension {dimension}'
        scale_map = {
            'V': 1e6,
            'mV': 1e3,
            'uV': 1,
        }
        return scale_map[dimension]

    def get_signal(self, ch_name=None, type='ecg', tmin=None, tmax=None, order=0, skip_dim=False):
        '''
        获取所有匹配信号，order代表次序，0代表第一个匹配的信号
        :param ch_name:
        :param type:
        :param tmin:
        :param tmax:
        :param order:
        :return:
        '''
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
            type = self.signal_type[idx]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        sfreq = int(self.reader.getSampleFrequency(idx))
        dimension = self.reader.getPhysicalDimension(idx)
        scale = 1
        if type in ['eeg', 'ecg']:
            scale = self._get_eeg_ecg_in_mV(dimension, skip_dim=skip_dim)
        if tmin is None or tmax is None:
            return self.reader.readSignal(idx) * scale
        start_samp_idx = sfreq * tmin
        end_samp_idx = sfreq * tmax
        n_samples = end_samp_idx - start_samp_idx
        return self.reader.readSignal(idx, start_samp_idx, n=n_samples) * scale

    def get_sample_frequency(self, ch_name=None, type='ecg', order=0):
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        return int(self.reader.getSampleFrequency(idx))

    def get_channel(self, ch_name=None, type=None, tmin=None, tmax=None, order=0):
        """
        获取信号和采样率，order代表次序，0代表第一个匹配的信号
        """
        signal = self.get_signal(ch_name, type, tmin, tmax, order)
        sampling_rate = self.get_sample_frequency(ch_name, type, order)
        return signal, sampling_rate

    def get_duration(self):
        return self.reader.file_duration


if __name__ == '__main__':
    fp = '/Users/cxs/Downloads/00001903-111140[001].edf'
    header = EDFHeaderParser(fp)
    header.get_signal_labels()
    reader = Base(fp)
    print(reader.get_signal(type='eeg', tmin=0, tmax=1))
    RR = reader.get_signal(ch_name="RR")
    plt.plot(RR)
    plt.show()
    sig = reader.get_signal(type='eeg')
    print(reader.signal_labels)
