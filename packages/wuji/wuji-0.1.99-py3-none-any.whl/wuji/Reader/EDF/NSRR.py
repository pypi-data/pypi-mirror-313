#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NSRR 
@Time        :   2023/8/17 16:47
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.Reader.EDF.Base import Base
import neurokit2 as nk
import numpy as np
import os, re


class NSRREDFReader(Base):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(file_path)

    def _assign_signal_types(self):
        super()._assign_signal_types()
        file_path = self.file_path
        pres_order, thermo_order = self.determine_pres_thermo_channel()
        values_to_find = ['nasal_thermometer', 'nasal_pressure', 'flow']
        matching_indices = np.where(np.in1d(self.signal_type, values_to_find))[0]
        if len(matching_indices) == 0:
            return

        try:
            if type(pres_order) == int:
                pres_idx = matching_indices[pres_order]
                # pres_idx = np.argwhere(self.signal_type == 'flow').flatten()[pres_order]
            elif type(pres_order) == str:
                pres_idx = np.argwhere(self.signal_labels == pres_order).flatten()[0]
            else:
                pres_idx = None

            if pres_idx is not None:
                self.signal_type[pres_idx] = 'nasal_pressure'
        except IndexError:
            pass

        try:
            if type(thermo_order) == int:
                thermo_idx = matching_indices[thermo_order]
            elif type(thermo_order) == str:
                thermo_idx = np.argwhere(self.signal_labels == thermo_order).flatten()[0]
            else:
                thermo_idx = None

            if thermo_idx is not None:
                self.signal_type[thermo_idx] = 'nasal_thermometer'
        except IndexError:
            pass

    def extract_subset_name(self):
        subset_name = None
        edf_name = os.path.basename(self.file_path).split('.')[0]
        sub_set_head = edf_name.split('-')[0]

        nsrr_non_mnc_set = ['mros', 'shhs', 'ccshs', 'cfs', 'chat', 'homepap', 'mesa']
        # 纯字母
        pattern1 = r'^[a-zA-Z]+'
        match1 = re.match(pattern1, sub_set_head)  # 'mros'，'shhs'，'ccshs'，'cfs'，'chat'，'homepap'，'mesa'，'sub'
        if match1 and match1.group() in nsrr_non_mnc_set:
            subset_name = match1.group()
            return subset_name

        # now determine if it is mnc subset
        sub_set_tail = edf_name.split('-')[-1]
        if not sub_set_tail.startswith('nsrr'):
            return None

        # 字母+数字
        pattern2 = r'^[a-zA-Z]+\d+'  # e.g. 'chp060','Sub89'
        match2 = re.match(pattern2, sub_set_head)
        if match2:
            matched_part = match2.group()
            if matched_part.startswith('chp'):
                subset_name = 'chp'
                return subset_name
            elif matched_part.startswith('Sub'):
                subset_name = 'Sub'
                return subset_name

        # 数字+字母
        pattern3 = r'^\d+[a-zA-Z]+'  # e.g. '161201f'
        match3 = re.match(pattern3, sub_set_head)
        if match3:
            subset_name = 'fhc'
            return subset_name

        # 纯数字
        pattern4 = r'^\d+'  # e.g. 16841809-nsrr.edf
        match4 = re.match(pattern4, sub_set_head)
        if match4:
            subset_name = 'khc'
            return subset_name

        # 其它：
        if sub_set_head.startswith('ssc'):
            subset_name = 'ssc'
        elif sub_set_head.startswith('al'):
            subset_name = 'al'
        elif sub_set_head.endswith('notte'):
            subset_name = 'notte'

        return subset_name

    def determine_pres_thermo_channel(self):
        """
        Determine the air and heat channel numbers based on the EDF file name.
        Args:
        edf_path (str): The path to the EDF file.
        Returns:
        tuple: A tuple containing the air channel number and the heat channel number.
        Raises:
        ValueError: If the psg_id is not recognized.
        """
        subset_name_prefix = self.extract_subset_name()
        channel_mapping = {
            'mros': (1, 0),
            'shhs': (None, 0),
            'ccshs': ('NASAL PRES', 0),
            'cfs': ('NASAL PRES', 0),
            'chat': (1, 0),
            'homepap': (1, 0),
            'mesa': ('Pres', 0),
            'sub': ('CFLOW', 'AIRFLOW'),
            'chp': (None, 'flow'),
            'Sub': (None, None),
            'fhc': (None, 'therm'),
            'khc': ('nas_pres', 'flow'),
            'ssc': ('nas_pres', 'therm'),
            'al': ('flow', 'therm'),
            'notte': (None, None)
        }

        # Get the channel numbers based on the PSG ID
        if subset_name_prefix in channel_mapping:
            nasal_pres_channel, nasal_thermo_channel = channel_mapping[subset_name_prefix]
        else:
            return None, None
        return nasal_pres_channel, nasal_thermo_channel


if __name__ == '__main__':
    fp = '/Users/cxs/project/OSAPillow/data/SHHS/edfs/shhs1-200001.edf'
    edf_path = r'C:\Users\46109\Downloads\mros-visit1-aa0570.edf'  # heat = 0 flow = 1
    # edf_path = r'C:\Users\46109\gry\nsrr_edf_samples\chp060-nsrr.edf'  # heat = flow
    # edf_path = r'C:\Users\46109\gry\nsrr_edf_samples\Sub89-nsrr.edf'  # None
    reader = NSRREDFReader(edf_path)
    # print(reader.get_signal(type='ecg', tmax=10))
    print(reader.get_signal(type='nasal_pressure', tmax=10))
    print(reader.get_signal(type='nasal_thermometer', tmax=10))
    # stages = Reader.get_standard_sleep_stages()
