#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NSRR 
@Time        :   2023/8/17 16:47
@Author      :   Xuesong Chen
@Description :   
"""
import os

import xmltodict
import pandas as pd

from wuji.Reader.Annotation.Base import Base, AHI, AHEventFilter
from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from datetime import datetime


class NSRRAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            info_dict = xmltodict.parse(f.read())
            self.scored_events = pd.DataFrame(info_dict['PSGAnnotation']['ScoredEvents']['ScoredEvent'])
            date_string = self.scored_events.loc[0, 'ClockTime']
            fake_datetime = datetime.strptime('2000-01-01 ' + date_string.split(' ')[-1], '%Y-%m-%d %H.%M.%S')
            self.recording_start_time = fake_datetime
            self.duration = float(self.scored_events.loc[0, 'Duration'])
            self.scored_events[['Start', 'Duration']] = self.scored_events[['Start', 'Duration']].astype(float)
            self.scored_events = self.scored_events.iloc[1:]

    def get_standard_sleep_stages(self):
        stages = self.scored_events[self.scored_events['EventType'] == 'Stages|Stages'].copy()
        stages.loc[:, 'stage_num'] = stages['EventConcept'].str.split('|', expand=True)[1].astype(int)
        map_dic = {0: 'Wake', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'N3', 5: 'REM'}
        stages.loc[:, 'Type'] = stages['stage_num'].map(map_dic)
        stages = stages[['Type', 'Start', 'Duration']]
        standard_stages = get_equal_duration_and_labeled_chunks(stages)
        self.sleep_stages = standard_stages
        return standard_stages

    def get_standard_AH_events(self, type='AHI3', od_eps=45, aro_eps=6):
        if type == 'AHI4':
            self.get_OD_events(OD_level=4)
            self.arousal_events = None
        elif type == 'AHI3':
            self.get_OD_events(OD_level=3)
            self.get_arousal_events()
        if self.respiratory_events is None:
            self.get_respiratory_events()
        filter = AHEventFilter(self.respiratory_events, self.OD_events, self.arousal_events, self.sleep_stages)
        self.OD_events = self.OD_events[['Type', 'Start', 'Duration', 'OD_level']]
        self.arousal_events = self.arousal_events[['Type', 'Start', 'Duration']]
        return filter.get_filtered_AH_events(type=type, od_eps=od_eps, aro_eps=aro_eps)

    def get_respiratory_events(self):
        res = self.scored_events[(self.scored_events['EventConcept'].str.contains('pnea'))
                                 | (self.scored_events['EventConcept'] == 'Unsure|Unsure')].copy()
        EventConcept_map = {
            'Hypopnea|Hypopnea': 'Hypopnea',
            'Obstructive apnea|Obstructive Apnea': 'Apnea',
            'Unsure|Unsure': 'Hyponpea',
            'Central apnea|Central Apnea': 'Apnea',
            'Mixed apnea|Mixed Apnea': 'Apnea',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        assert res['Type'].isna().sum() == 0, f"存在未map的呼吸事件:{res['EventConcept'].unique()}"
        self.respiratory_events = res[['Type', 'Start', 'Duration']][(res['Duration'] >= 10) & (res['Duration'] <= 120)]
        self.respiratory_events.reset_index(drop=True, inplace=True)
        return self.respiratory_events

    def get_OD_events(self, OD_level=4):
        res = self.scored_events[(self.scored_events['EventConcept'] != 'Wake|0') &
                                 (self.scored_events['EventConcept'] == 'SpO2 desaturation|SpO2 desaturation')].copy()
        if res.empty:
            self.OD_events = pd.DataFrame(columns=['Type', 'Start', 'Duration', 'OD_level'])
            return self.OD_events
        EventConcept_map = {
            'SpO2 desaturation|SpO2 desaturation': 'OD',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        res['OD_level'] = res['SpO2Baseline'].astype(float) - res['SpO2Nadir'].astype(float)
        self.OD_events = res[['Type', 'Start', 'Duration', 'OD_level']][(res['OD_level'] >= OD_level)]
        self.OD_events.reset_index(drop=True, inplace=True)
        return self.OD_events

    def get_arousal_events(self):
        res = self.scored_events[(self.scored_events['EventConcept'] != 'Wake|0') &
                                 (self.scored_events['EventConcept'] == 'Arousal|Arousal ()')].copy()
        EventConcept_map = {
            'Arousal|Arousal ()': 'Arousal',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        self.arousal_events = res[['Type', 'Start', 'Duration']]
        self.arousal_events.reset_index(drop=True, inplace=True)
        return self.arousal_events


if __name__ == '__main__':
    import warnings
    from wuji.Reader.EDF.NSRR import NSRREDFReader

    warnings.filterwarnings('ignore')
    for file in sorted(os.listdir('/Users/cxs/project/OSAPillow/data/SHHS/annotations')):
        if file.endswith('.xml'):
            fp = os.path.join('/Users/cxs/project/OSAPillow/data/SHHS/annotations', file)
            reader = NSRRAnnotationReader(fp)
            stages = reader.get_standard_sleep_stages()
            AH_events = reader.get_standard_AH_events(type='AHI3')
            ahi_calculator = AHI(AH_events, stages)
            ahi = ahi_calculator.get_AHI(type='Total')
            print(f'{file} AHI: {round(ahi, 2)}')
