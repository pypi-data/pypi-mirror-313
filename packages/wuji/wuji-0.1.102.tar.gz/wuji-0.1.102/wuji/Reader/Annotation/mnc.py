#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   mnc 
@Time        :   2024/10/14 14:32
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.Reader.Annotation.Base import Base
import xmltodict
import pandas as pd
from datetime import datetime


class MNCAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            info_dict = xmltodict.parse(f.read())
            self.scored_events = pd.DataFrame(info_dict['Annotations']['Instances']['Instance'])
            fake_date = datetime.strptime('2000-01-01', '%Y-%m-%d')
            start_time = datetime.strptime(info_dict['Annotations']['StartTime'], '%H.%M.%S')
            fake_datetime = datetime(
                fake_date.year, fake_date.month, fake_date.day,
                start_time.hour, start_time.minute, start_time.second
            )
            self.recording_start_time = fake_datetime
            self.duration = len(self.scored_events) * 30

    def get_standard_sleep_stages(self):
        stages = self.scored_events.copy()
        map_dic = {'wake': 'Wake', 'NREM1': 'N1', 'NREM2': 'N2', 'NREM3': 'N3', 'REM': 'REM'}
        all_stages = stages['@class'].unique()
        assert all([stage in map_dic.keys() for stage in all_stages]), f"Unknown sleep stage: {all_stages}"
        stages['Type'] = stages['@class'].map(map_dic)
        self.sleep_stages = stages[['Type', 'Start', 'Duration']]
        return self.sleep_stages

    def get_standard_AH_events(self):
        return None

    def get_respiratory_events(self):
        return None

    def get_OD_events(self):
        return None

    def get_arousal_events(self):
        return None


if __name__ == '__main__':
    fp = "/Users/cxs/Downloads/mnc/N0081-nsrr.xml"
    reader = MNCAnnotationReader(fp)
    print(reader.get_standard_sleep_stages())
