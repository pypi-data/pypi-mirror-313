#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Philips 
@Time        :   2023/9/14 15:41
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.Reader.EDF.Base import Base
import numpy as np
import os


class PhilipsEDFReader(Base):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(file_path)

    def determine_air_nasal_channel(self):
        """
        Determine the air and heat channel numbers based on the EDF file name.
        Args:
        edf_path (str): The path to the EDF file.
        Returns:
        tuple: A tuple containing the air channel number and the heat channel number.
        Raises:
        ValueError: If the psg_id is not recognized.
        """
        edf_name = os.path.basename(self.file_path).split('.')[0]
        psg_id = edf_name.split('-')[1].split('_')[0]
        channel_mapping = {
            'LEBS20454': (1, 0),
            'A5BS14772': (2, 1),
            '113072': (1, 0),
            '111298': (1, 0),
            '110474': (1, 0),
            '100564': (1, 0),
            '111032': (1, 0),
            '113080': (1, 0),
            '100632': (1, 0),
            '101030': (1, 0),
            '110488': (1, 0),
            '111034': (2, 0),
            '111079': (1, 0),
            '111275': (1, 0),
            '111276': (1, 0),
            '111278': (1, 0),
            '114463': (2, 1),
            'LEBS21876': (1, 0)
        }

        # Get the channel numbers based on the PSG ID
        if psg_id in channel_mapping:
            air_channel, nasal_channel = channel_mapping[psg_id]
        else:
            raise ValueError(f"Unknown psg_id: {psg_id} in determine_air_nasal_channel, file_name: {edf_name}")

        return air_channel, nasal_channel

    def _assign_signal_types(self):
        super()._assign_signal_types()
        try:
            airflow_order, nasal_order = self.determine_air_nasal_channel()
            airflow_idx = np.argwhere(self.signal_type == 'flow').flatten()[airflow_order]
            nasal_idx = np.argwhere(self.signal_type == 'flow').flatten()[nasal_order]
            self.signal_type[airflow_idx] = 'nasal_pressure'
            self.signal_type[nasal_idx] = 'nasal_thermometer'
        except:
            pass